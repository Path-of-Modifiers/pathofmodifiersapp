import { Box, Divider } from "@chakra-ui/layout";
import { TextRollInput } from "./TextRollInput";
import {
  MinMaxNumberInput,
  DefaultMinMaxValues,
} from "../StandardLayoutInput/MinMaxNumberInput";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { WantedModifierSpecs } from "../../../store/StateInterface";

type HandleChangeEventFunction = (
  isNumerical: boolean,
  modifierId: number,
  value: string | undefined,
  selectedModifierIndex: number,
  numericalType?: string,
  textRolls?: string
) => void;

export type TakingInputEventFunction = (orderIndex: number) => void;

interface InputChangeHandler {
  modifierId: number;
  selectedModifierIndex: number;
  currentRelevantModifierSpec: WantedModifierSpecs;
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
            props.isNumerical,
            props.modifierId,
            value,
            props.selectedModifierIndex,
            numericalType
          )
        }
        flexProps={{
          onBlur: () => props.changeTakingInput(props.orderIndex),
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
    if (defaultTextIndex) {
      defaultTextValue = textRolls.split("|")[defaultTextIndex];
    }
    return (
      <TextRollInput
        textRolls={textRolls}
        index={props.selectedModifierIndex}
        handleTextChange={(value) =>
          props.handleAnyChange(
            props.isNumerical,
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
        }}
      ></TextRollInput>
    );
  }
};

interface DefaultOutputHandlerProps {
  currentRelevantModifierSpec: WantedModifierSpecs;
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
    wantedModifierSpecs,
    setWantedModifierMinRoll,
    setWantedModifierMaxRoll,
    setWantedModifierTextRoll,
  } = useGraphInputStore();

  // A generic handle function that handles mixed input
  const handleAnyChange: HandleChangeEventFunction = (
    isNumerical: boolean,
    modifierId: number,
    value: string | undefined,
    selectedModifierIndex: number,
    numericalType?: string,
    textRolls?: string
  ): void => {
    if (isNumerical && numericalType !== undefined) {
      const numValue = value !== undefined ? Number(value) : undefined;
      if (numericalType === "min") {
        setWantedModifierMinRoll(modifierId, numValue, selectedModifierIndex);
      } else if (numericalType === "max") {
        setWantedModifierMaxRoll(modifierId, numValue, selectedModifierIndex);
      } else {
        throw `numerical type needs to be 'min' or 'max', not ${numericalType}`;
      }
    } else if (isNumerical && numericalType === undefined) {
      throw "Numerical type must be specified if 'isNumerical`===true";
    } else if (!isNumerical && textRolls) {
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
  const currentWantedModifierSpecs = wantedModifierSpecs.filter(
    (spec) => spec.index == props.selectedModifierIndex
  );
  if (wantedModifierSpecs === undefined) {
    throw `Couldnt find the current 'wantedModifierSpecs' with the index ${props.selectedModifierIndex}`;
  }
  const currentRelevantModifierSpec =
    currentWantedModifierSpecs[props.orderIndex];

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
