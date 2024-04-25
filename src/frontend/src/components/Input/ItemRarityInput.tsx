import { Select } from "@chakra-ui/react";
import { RenderInputProps } from "./ModifierInput";

const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  const selectedValue = event.target.value;
};

export const ItemRarityInput = () => {
  return (
    <Select
      bgColor={"ui.input"}
      defaultValue={"TextRolls"}
      onChange={(e) => handleChange(e)}
      width={150}
      focusBorderColor={"ui.white"}
      borderColor={"ui.grey"}
      mr={1}
      ml={1}
      key={"ItemRarityInput"}
    >
      {
        <option
          value={"undefined"}
          key={"ItemRarityInput" + "_option_" + "Unique"}
          style={{ color: "#B3B3B3", backgroundColor: "#2d3333" }}
        >
          Unique
        </option>
      }
    </Select>
  );
};
