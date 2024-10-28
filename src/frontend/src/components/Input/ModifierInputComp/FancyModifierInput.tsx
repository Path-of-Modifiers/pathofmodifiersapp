import { Box, Divider } from "@chakra-ui/layout";
import { TextRollInput } from "./TextRollInput";
import {
  MinMaxNumberInput,
  DefaultMinMaxValues,
} from "../StandardLayoutInput/MinMaxNumberInput";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { WantedModifierExtended } from "../../../store/StateInterface";

type HandleChangeEventFunction = (
  modifierId: number,
  value: string | undefined,
  selectedModifierIndex: number,
  numericalType?: "min" | "max",
  textRolls?: string
) => void;

export type TakingInputEventFunction = (orderIndex: number) => void;

interface InputChangeHandler {
  modifierId: number;
  selectedModifierIndex: number;
  currentRelevantModifierSpec: WantedModifierExtended;
  orderIndex: number;
  isNumerical: boolean;
  textRolls: string | null | undefined;
  handleAnyChange: HandleChangeEventFunction;
  changeTakingInput: TakingInputEventFunction;
}

const InputChangeHandler = (props: InputChangeHandler) => {
  const modifierLimitations =
    props.currentRelevantModifierSpec.modifierLimitations;
  const textRolls = props.textRolls;
  if (props.isNumerical) {
    const defaultMinMaxValues: DefaultMinMaxValues = {
      max: modifierLimitations?.maxRoll ?? undefined,
      min: modifierLimitations?.minRoll ?? undefined,
    };
    return (
      <MinMaxNumberInput
        handleNumberChange={(value, numericalType) =>
          props.handleAnyChange(
            props.modifierId,
            value,
            props.selectedModifierIndex,
            numericalType
          )
        }
        flexProps={{
          onBlur: () => props.changeTakingInput(props.orderIndex),
          mt: "auto",
        }}
        defaultValues={defaultMinMaxValues}
        tight={true}
      />
    );
  } else if (textRolls == null) {
    throw "'textRolls' cannot be undefined at the same time as 'isNumerical===false'";
  } else {
    const defaultTextIndex = modifierLimitations?.textRoll ?? undefined;
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
            value,
            props.selectedModifierIndex,
            undefined,
            textRolls
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
  currentRelevantModifierSpec: WantedModifierExtended;
  isNumerical: boolean;
  textRolls: string | null | undefined;
}

const DefaultOutputHandler = (props: DefaultOutputHandlerProps) => {
  const modifierLimitations =
    props.currentRelevantModifierSpec.modifierLimitations;
  if (modifierLimitations == null) {
    return <Box as="u">#</Box>;
  }
  if (props.isNumerical) {
    if (
      modifierLimitations.minRoll == null &&
      modifierLimitations.maxRoll == null
    ) {
      return <Box as="u">#</Box>;
    }
    return (
      <Box>
        <Box fontSize={10} textAlign="center">
          {modifierLimitations.minRoll ? modifierLimitations.minRoll : "Min"}
        </Box>
        <Divider borderColor="ui.queryMainInput" />
        <Box fontSize={10} textAlign="center">
          {modifierLimitations.maxRoll ? modifierLimitations.maxRoll : "Max"}
        </Box>
      </Box>
    );
  } else if (props.textRolls == null) {
    throw "'textRolls' cannot be undefined at the same time as 'isNumerical===false'";
  } else {
    return (
      <Box as="u">
        {modifierLimitations.textRoll != null
          ? props.textRolls.split("|")[modifierLimitations.textRoll]
          : "#"}
      </Box>
    );
  }
};

interface FancyModifierInputProps {
  currentlyTakingInput: boolean;
  modifierId: number;
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
    value: string | undefined,
    selectedModifierIndex: number,
    numericalType?: "min" | "max",
    textRolls?: string
  ): void => {
    if (numericalType && textRolls) {
      throw "'numericalType' and 'textRolls' cannot both be defined";
    }
    if (numericalType !== undefined) {
      const numValue = value ? Number(value) : undefined;
      if (numericalType === "min") {
        setWantedModifierMinRoll(modifierId, numValue, selectedModifierIndex);
      } else {
        setWantedModifierMaxRoll(modifierId, numValue, selectedModifierIndex);
      }
    } else if (textRolls) {
      if (value === "Any") {
        value = undefined;
      }
      const textValue =
        value !== undefined ? textRolls.split("|").indexOf(value) : undefined;
      setWantedModifierTextRoll(modifierId, textValue, selectedModifierIndex);
    } else {
      throw "Modifier must have text rolls if the roll is not numerical.";
    }
  };
  if (wantedModifierExtended === undefined) {
    throw `Couldnt find the current 'wantedModifierExtended' with the index ${props.selectedModifierIndex}`;
  }
  const currentWantedModifierExtended = wantedModifierExtended.filter(
    (spec) => spec.index == props.selectedModifierIndex
  );

  const currentRelevantModifierSpec =
    currentWantedModifierExtended[props.orderIndex];

  // console.log("asbdhbasdhv", currentWantedModifierExtended);
  // console.log("dasdas", currentRelevantModifierSpec);
  // This happens when 'Clear Query' is pressed:
  // For a split second this element is rerendered, but there are no selected modifiers.
  // which makes 'currentRelevantModifierSpec' null | undefined
  if (currentRelevantModifierSpec == null) {
    return;
  }

  if (props.currentlyTakingInput) {
    return (
      <InputChangeHandler
        modifierId={props.modifierId}
        currentRelevantModifierSpec={currentRelevantModifierSpec}
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
          currentRelevantModifierSpec={currentRelevantModifierSpec}
          isNumerical={isNumerical}
          textRolls={props.textRolls}
        />
      </Box>
    );
  }
};
