import { Box, Select } from "@chakra-ui/react";
import { useGraphInputStore } from "../../store/GraphInputStore";

const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  const itemRarityInput = event.target.value;
  useGraphInputStore.setState({ itemSpecState: itemRarityInput });
};

export const ItemRarityInput = () => {
  return (
    <Box>
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
        ,
        {
          <option
            value={"Non_Unique"}
            key={"ItemRarityInput" + "_option_" + "Any Non-Unique"}
            style={{ color: "#B3B3B3", backgroundColor: "#2d3333" }}
          >
            Any Non-Unique
          </option>
        }
      </Select>
    </Box>
  );
};
