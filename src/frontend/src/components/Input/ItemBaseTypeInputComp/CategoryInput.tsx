import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { GetItemBaseTypeCategories } from "../../../hooks/getBaseTypeCategories";
import { ItemBaseTypeCategory } from "../../../client";
import { capitalizeFirstLetter } from "../../../hooks/utils";

const handleCategoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  const itemCategory = event.target.value;
  useGraphInputStore.setState({ baseSpec: { category: itemCategory } });
};

export const CategoryInput = () => {
  const categories: ItemBaseTypeCategory[] | undefined =
    GetItemBaseTypeCategories();

  let categoryOptions: JSX.Element[] = [];
  if (categories !== undefined) {
    categoryOptions = categories.map((baseCategory) => {
      return (
        <option
          value={capitalizeFirstLetter(baseCategory.category)}
          key={"ItemCategoryInput" + "_option_" + baseCategory.category}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          {capitalizeFirstLetter(baseCategory.category)}
        </option>
      );
    });
  }

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
        {categoryOptions}
      </Select>
    </Flex>
  );
};
