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

// Function to handle the change of the max roll input value
const handleChange = (
  eventValue: string,
  inputPosition: number,
  modifierSelected: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction // Function to update the modifier input
) => {
  // If the max roll input is defined, set the value of the input at the input position to the event value
  if (modifierSelected.maxRollInputs) {
    modifierSelected.maxRollInputs[inputPosition] = parseFloat(eventValue);
  } else {
    modifierSelected.maxRollInputs = [parseFloat(eventValue)];
  }
  updateModifierInputFunction(
    modifierSelected.modifierId[inputPosition],
    undefined,
    modifierSelected.maxRollInputs.map((input) => input),
    undefined
  );
};

// Max Roll Input Component  -  This component is used to input the maximum roll of a modifier
export const MaxRollInput = ({
  modifierSelected,
  inputPosition,
  updateModifierInputFunction,
}: RenderInputMaxMinRollProps) => {
  if (!modifierSelected.maxRoll) {
    return null;
  }

  return (
    <NumberInput
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
