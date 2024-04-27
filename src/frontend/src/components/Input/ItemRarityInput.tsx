import { Select } from "@chakra-ui/react";

const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  console.log(event.target.value);
};

export const ItemRarityInput = () => {
  return (
    <Select
      bgColor={"ui.input"}
      color={"ui.white"}
      defaultValue={"Unique"}
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
          value={"Unique"}
          key={"ItemRarityInput" + "_option_" + "Unique"}
          style={{ color: "#B3B3B3", backgroundColor: "#2d3333" }}
        >
          Unique
        </option>
      }
    </Select>
  );
};
