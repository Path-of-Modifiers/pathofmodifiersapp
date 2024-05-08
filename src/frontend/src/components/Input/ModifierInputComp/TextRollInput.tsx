import { Select } from "@chakra-ui/react";
import {
  ModifierInput,
  RenderInputProps,
  UpdateModifierInputFunction,
} from "./ModifierInput";

// Function to handle the change of the text roll input value
const handleChange = (
  event: React.ChangeEvent<HTMLSelectElement>,
  inputPosition: number,
  modifierSelected: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction // Function to update the modifier input
) => {
  const selectedValue = parseInt(event.target.value); // Parse the selected value to an integer

  // If the text roll input is defined, set the value of the input at the input position to the event value
  if (modifierSelected.textRollInputs) {
    modifierSelected.textRollInputs[inputPosition] = selectedValue;
  } else {
    modifierSelected.textRollInputs = [selectedValue];
  }
  updateModifierInputFunction(
    modifierSelected.modifierId[inputPosition],
    undefined,
    undefined,
    modifierSelected.textRollInputs
  );
};

// Text Roll Input Component  -  This component is used to select the text roll of a modifier
export const TextRollInput = ({
  modifierSelected,
  inputPosition,
  updateModifierInputFunction,
}: RenderInputProps) => {
  if (!modifierSelected.textRolls) {
    return null;
  }
  // Get the text rolls of the modifier at the input position
  const textRolls = modifierSelected.textRolls[inputPosition] as string;
  const textRollsList = textRolls.split("-"); // Split the text rolls into a list

  // Create the text roll options
  const textRollsOptions = textRollsList.map((textRoll, index) => (
    <option
      value={index}
      key={modifierSelected.effect + textRoll + index}
      style={{ backgroundColor: "#2d3333" }}
    >
      {textRoll}
    </option>
  ));

  return (
    <Select
      bgColor={"ui.input"}
      defaultValue={"TextRolls"}
      onChange={(e) =>
        handleChange(
          e,
          inputPosition,
          modifierSelected,
          updateModifierInputFunction
        )
      }
      width={150}
      focusBorderColor={"ui.white"}
      borderColor={"ui.grey"}
      mr={1}
      ml={1}
      key={modifierSelected.effect + inputPosition}
    >
      {
        <option
          value={"undefined"}
          key={modifierSelected.effect + "undefined"}
          style={{ color: "#B3B3B3", backgroundColor: "#2d3333" }}
        >
          Any
        </option>
      }
      {textRollsOptions}
    </Select>
  );
};
