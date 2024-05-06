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

const handleChange = (
  eventValue: string,
  inputPosition: number,
  modifierSelected: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
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
