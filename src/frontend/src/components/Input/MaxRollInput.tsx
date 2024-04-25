import {
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
} from "@chakra-ui/react";
import {
  ModifierInput,
  RenderInputMaxMinRollProps,
  UpdateModifierInputFunction,
} from "../Graph/ModifierInput";

const handleInputMaxRollChange = (
  value: string,
  position: number,
  modifier: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
  if (modifier.maxRollInputs) {
    modifier.maxRollInputs[position] = value;
  } else {
    modifier.maxRollInputs = [value];
  }
  updateModifierInputFunction(
    modifier.modifierId[position],
    undefined,
    undefined,
    modifier.maxRollInputs
  );
};

const handleChange = (
  eventValue: string,
  inputPosition: number,
  modifierSelected: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
  const selectedValue = eventValue;
  // Call function to handle the change
  handleInputMaxRollChange(
    selectedValue,
    inputPosition,
    modifierSelected,
    updateModifierInputFunction
  );
};

export const MaxRollInput = ({
  modifierSelected,
  input,
  inputPosition,
  updateModifierInputFunction,
}: RenderInputMaxMinRollProps) => {
  if (!modifierSelected.maxRoll) {
    return null;
  }
  const defaultValue = modifierSelected.maxRoll[inputPosition] as number;

  return (
    <NumberInput
      value={input ? input : defaultValue}
      defaultValue={defaultValue}
      step={1}
      key={modifierSelected.modifierId[0] + inputPosition}
      bgColor={"ui.input"}
      focusBorderColor={"ui.white"}
      borderColor={"ui.grey"}
      onChange={(e) =>
        handleChange(
          e,
          inputPosition,
          modifierSelected,
          updateModifierInputFunction
        )
      }
      width={"30%"}
      mr={1}
      _placeholder={{ color: "ui.white" }}
      textAlign={"center"}
    >
      <NumberInputField />
      <NumberInputStepper>
        <NumberIncrementStepper />
        <NumberDecrementStepper />
      </NumberInputStepper>
    </NumberInput>
  );
};
