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
} from "./ModifierInput";

const handleInputMaxRollChange = (
  value: string,
  position: number,
  modifier: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
  if (modifier.maxRollInputs) {
    modifier.maxRollInputs[position] = parseInt(value);
  } else {
    modifier.maxRollInputs = [parseInt(value)];
  }
  updateModifierInputFunction(
    modifier.modifierId[position],
    undefined,
    modifier.maxRollInputs.map((input) => input),
    undefined
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

  return (
    <NumberInput
      value={input ? input : undefined}
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
      width={150}
      mr={1}
      ml={1}
      _placeholder={{ color: "ui.white" }}
      textAlign={"center"}
    >
      <NumberInputField placeholder={"Max"} />
      <NumberInputStepper>
        <NumberIncrementStepper />
        <NumberDecrementStepper />
      </NumberInputStepper>
    </NumberInput>
  );
};
