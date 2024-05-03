import { Select } from "@chakra-ui/react";
import {
  ModifierInput,
  RenderInputProps,
  UpdateModifierInputFunction,
} from "./ModifierInput";

const handleInputTextRollChange = (
  value: number,
  position: number,
  modifier: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
  if (modifier.textRollInputs) {
    modifier.textRollInputs[position] = value;
  } else {
    modifier.textRollInputs = [value];
  }
  updateModifierInputFunction(
    modifier.modifierId[position],
    undefined,
    undefined,
    modifier.textRollInputs
  );
};

const handleChange = (
  event: React.ChangeEvent<HTMLSelectElement>,
  inputPosition: number,
  modifierSelected: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
  const selectedValue = parseInt(event.target.value);
  // Call function to handle the change
  handleInputTextRollChange(
    selectedValue,
    inputPosition,
    modifierSelected,
    updateModifierInputFunction
  );
};

export const TextRollInput = ({
  modifierSelected,
  inputPosition,
  updateModifierInputFunction,
}: RenderInputProps) => {
  if (!modifierSelected.textRolls) {
    return null;
  }
  const textRolls = modifierSelected.textRolls[inputPosition] as string;
  const textRollsList = textRolls.split("-");

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
