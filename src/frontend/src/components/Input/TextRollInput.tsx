import { Select } from "@chakra-ui/react";
import {
  ModifierInput,
  UpdateModifierInputFunction,
} from "../Graph/ModifierInput";

interface RenderInputProps {
  modifierSelected: ModifierInput;
  inputPosition: number;
  updateModifierInputFunction: UpdateModifierInputFunction;
}

const handleInputChange = (
  value: string,
  position: number,
  modifier: ModifierInput,
  updateModifierInputFunction: UpdateModifierInputFunction
) => {
  // Regular expression to allow numbers and scientific notation
  // const scientificPattern = /^-?\d*\.?\d*(e-?\d+)?$/i;

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
  const selectedValue = event.target.value;
  // Call function to handle the change
  handleInputChange(
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
  console.log("BEAST YES");
  console.log("modifierSelected: ", modifierSelected);
  if (!modifierSelected.textRolls) {
    return null;
  }
  const textRolls = modifierSelected.textRolls[inputPosition] as string;
  const textRollsList = textRolls.split("-");

  const textRollsOptions = textRollsList.map((textRoll, index) => (
    <option
      value={textRoll}
      key={modifierSelected.effect + textRoll + index}
      style={{ backgroundColor: "#2d3333" }}
    >
      {textRoll}
    </option>
  ));

  return (
    <>
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
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        width={"40%"}
        mr={1}
        key={modifierSelected.effect + inputPosition}
      >
        {textRollsOptions}
      </Select>
    </>
  );
};
