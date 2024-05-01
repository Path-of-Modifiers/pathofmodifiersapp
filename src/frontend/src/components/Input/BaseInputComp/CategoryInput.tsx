import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

const handleCategoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  const itemCategory = event.target.value;
  useGraphInputStore.setState({ baseSpec: { category: itemCategory } });
  // console.log(useGraphInputStore.getState().itemSpecState);
};

// const handleSubCategoryChange = (
//   event: React.ChangeEvent<HTMLSelectElement>
// ) => {
//   const itemSubCategory = event.target.value;
//   useGraphInputStore.setState({ baseSpec: { subCategory: itemSubCategory } });
//   // console.log(useGraphInputStore.getState().itemSpecState);
// };

export const CategoryInput = () => {
  return (
    <Flex
      alignItems={"center"}
      color={"ui.white"}
      bgColor={"ui.secondary"}
      m={1}
    >
      <Text ml={1} width={150}>
        Item Category
      </Text>
      <Select
        bgColor={"ui.input"}
        color={"ui.white"}
        defaultValue={"Unique"}
        onChange={(e) => handleCategoryChange(e)}
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
          // Future implementation for non-unique items
          // <option
          //   value={"Non_Unique"}
          //   key={"ItemRarityInput" + "_option_" + "Any Non-Unique"}
          //   style={{ color: "#B3B3B3", backgroundColor: "#2d3333" }}
          // >
          //   Any Non-Unique
          // </option>
        }
      </Select>
    </Flex>
  );
};
