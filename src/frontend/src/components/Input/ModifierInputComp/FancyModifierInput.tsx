import { Box, Divider } from "@chakra-ui/layout";
import { TextRollInput } from "./TextRollInput";
import {
  MinMaxNumberInput,
  DefaultMinMaxValues,
} from "../StandardLayoutInput/MinMaxNumberInput";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { ModifierLimitationState } from "../../../store/StateInterface";

type HandleChangeEventFunction = (
  modifierId: number,
  position: number,
  value: string | undefined,
  selectedModifierIndex: number,
  numericalType?: "min" | "max",
  textRolls?: string,
) => void;

export type TakingInputEventFunction = (orderIndex: number) => void;

interface InputChangeHandler {
  modifierId: number;
  position: number;
  selectedModifierIndex: number;
  modifierLimitation: ModifierLimitationState | null | undefined;
  orderIndex: number;
  isNumerical: boolean;
  textRolls: string | null | undefined;
  handleAnyChange: HandleChangeEventFunction;
  changeTakingInput: TakingInputEventFunction;
}

const InputChangeHandler = (props: InputChangeHandler) => {
  const textRolls = props.textRolls;
  if (props.isNumerical) {
    const defaultMinMaxValues: DefaultMinMaxValues = {
      max: props.modifierLimitation?.maxRoll ?? undefined,
      min: props.modifierLimitation?.minRoll ?? undefined,
    };
    return (
      <MinMaxNumberInput
        handleNumberChange={(value, numericalType) =>
          props.handleAnyChange(
            props.modifierId,
            props.position,
            value,
            props.selectedModifierIndex,
            numericalType,
          )
        }
        flexProps={{
          onBlur: () => props.changeTakingInput(props.orderIndex),
          mt: "auto",
        }}
        defaultValues={defaultMinMaxValues}
        tight={true}
        autoFocus={true}
      />
    );
  } else if (textRolls == null) {
    throw "'textRolls' cannot be undefined at the same time as 'isNumerical===false'";
  } else {
    const defaultTextIndex = props.modifierLimitation?.textRoll ?? undefined;
    let defaultTextValue: string | undefined = undefined;
    if (defaultTextIndex !== undefined) {
      defaultTextValue = textRolls.split("|")[defaultTextIndex];
    }
    return (
      <TextRollInput
        textRolls={textRolls}
        index={props.selectedModifierIndex}
        handleTextChange={(value) =>
          props.handleAnyChange(
            props.modifierId,
            props.position,
            value,
            props.selectedModifierIndex,
            undefined,
            textRolls,
          )
        }
        defaultValue={defaultTextValue}
        flexProps={{
          onBlur: () => props.changeTakingInput(props.orderIndex),
          mt: "-10.5px",
        }}
      ></TextRollInput>
    );
  }
};

interface DefaultOutputHandlerProps {
  modifierLimitation: ModifierLimitationState | null | undefined;
  isNumerical: boolean;
  textRolls: string | null | undefined;
}

const DefaultOutputHandler = (props: DefaultOutputHandlerProps) => {
  if (props.modifierLimitation == null) {
    return <Box as="u">#</Box>;
  }
  if (props.isNumerical) {
    if (
      props.modifierLimitation.minRoll == null &&
      props.modifierLimitation.maxRoll == null
    ) {
      return <Box as="u">#</Box>;
    }
    return (
      <Box>
        <Box fontSize={10} textAlign="center">
          {props.modifierLimitation.minRoll
            ? props.modifierLimitation.minRoll
            : "Min"}
        </Box>
        <Divider borderColor="ui.queryMainInput" />
        <Box fontSize={10} textAlign="center">
          {props.modifierLimitation.maxRoll
            ? props.modifierLimitation.maxRoll
            : "Max"}
        </Box>
      </Box>
    );
  } else if (props.textRolls == null) {
    throw "'textRolls' cannot be undefined at the same time as 'isNumerical===false'";
  } else {
    return (
      <Box as="u">
        {props.modifierLimitation.textRoll != null
          ? props.textRolls.split("|")[props.modifierLimitation.textRoll]
          : "#"}
      </Box>
    );
  }
};

interface FancyModifierInputProps {
  currentlyTakingInput: boolean;
  modifierId: number;
  position: number;
  selectedModifierIndex: number;
  textRolls: string | null | undefined;
  orderIndex: number;
  changeTakingInput: TakingInputEventFunction;
}

export const FancyModifierInput = (props: FancyModifierInputProps) => {
  const isNumerical = props.textRolls == null;
  const {
    wantedModifierExtended,
    setWantedModifierMinRoll,
    setWantedModifierMaxRoll,
    setWantedModifierTextRoll,
  } = useGraphInputStore();

  // A generic handle function that handles mixed input
  const handleAnyChange: HandleChangeEventFunction = (
    modifierId: number,
    position: number,
    value: string | undefined,
    selectedModifierIndex: number,
    numericalType?: "min" | "max",
    textRolls?: string,
  ): void => {
    if (numericalType && textRolls) {
      throw "'numericalType' and 'textRolls' cannot both be defined";
    }
    if (numericalType !== undefined) {
      const numValue = value ? Number(value) : undefined;
      if (numericalType === "min") {
        setWantedModifierMinRoll(
          modifierId,
          position,
          numValue,
          selectedModifierIndex,
        );
      } else {
        setWantedModifierMaxRoll(
          modifierId,
          position,
          numValue,
          selectedModifierIndex,
        );
      }
    } else if (textRolls) {
      if (value === "Any") {
        value = undefined;
      }
      const textValue =
        value !== undefined ? textRolls.split("|").indexOf(value) : undefined;
      setWantedModifierTextRoll(
        modifierId,
        position,
        textValue,
        selectedModifierIndex,
      );
    } else {
      throw "Modifier must have text rolls if the roll is not numerical.";
    }
  };
  if (wantedModifierExtended === undefined) {
    throw `Couldnt find the current 'wantedModifierExtended' with the index ${props.selectedModifierIndex}`;
  }
  const currentWantedModifierExtended = wantedModifierExtended.filter(
    (spec) => spec.index == props.selectedModifierIndex,
  );

  const currentModifierLimitations = currentWantedModifierExtended.find(
    (wantedModifierExtended) =>
      wantedModifierExtended.modifierId === props.modifierId &&
      wantedModifierExtended.index === props.selectedModifierIndex,
  )?.modifierLimitations;

  let currentModifierPositionLimitation:
    | ModifierLimitationState
    | null
    | undefined = null;
  if (currentModifierLimitations != null) {
    currentModifierPositionLimitation = currentModifierLimitations?.find(
      (limitation) => limitation.position === props.position,
    );
  }

  // This happens when 'Clear Query' is pressed:
  // For a split second this element is rerendered, but there are no selected modifiers.
  // which makes 'currentModifierLimitations' null | undefined
  // if (currentModifierLimitations == null) {
  //   return;
  // }

  if (props.currentlyTakingInput) {
    return (
      <InputChangeHandler
        modifierId={props.modifierId}
        position={props.position}
        modifierLimitation={currentModifierPositionLimitation}
        selectedModifierIndex={props.selectedModifierIndex}
        orderIndex={props.orderIndex}
        isNumerical={isNumerical}
        textRolls={props.textRolls}
        handleAnyChange={handleAnyChange}
        changeTakingInput={props.changeTakingInput}
      />
    );
  } else {
    return (
      <Box
        onClick={() => props.changeTakingInput(props.orderIndex)}
        color="ui.queryMainInput"
        key={`fancyInput-${props.selectedModifierIndex}-click-${props.orderIndex}`}
      >
        <DefaultOutputHandler
          modifierLimitation={currentModifierPositionLimitation}
          isNumerical={isNumerical}
          textRolls={props.textRolls}
        />
      </Box>
    );
  }
};
