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

// Function to handle the change of the min roll input value
const handleChange = (
  eventValue: string,
  inputPosition: number,
  modifierSelected: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction // Function to update the modifier input
) => {
  // If the min roll input is defined, set the value of the input at the input position to the event value
  if (modifierSelected.minRollInputs) {
    modifierSelected.minRollInputs[inputPosition] = parseFloat(eventValue);
  } else {
    modifierSelected.minRollInputs = [parseFloat(eventValue)];
  }

  updateModifierInputFunction(
    modifierSelected.modifierId[inputPosition],
    modifierSelected.minRollInputs.map((input) => (input ? input : null)),
    undefined,
    undefined
  );
};

// Min Roll Input Component  -  This component is used to input the minimum roll of a modifier
export const MinRollInput = ({
  modifierSelected,
  inputPosition,
  updateModifierInputFunction,
}: RenderInputMaxMinRollProps) => {
  if (!modifierSelected.minRoll) {
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
      <NumberInputField placeholder={"Min"} />
      <NumberInputStepper>
        <NumberIncrementStepper />
        <NumberDecrementStepper />
      </NumberInputStepper>
    </NumberInput>
  );
};
