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
      precision={2}
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
