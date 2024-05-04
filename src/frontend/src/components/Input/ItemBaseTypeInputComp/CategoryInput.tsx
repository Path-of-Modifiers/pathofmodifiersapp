import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import { ItemBaseTypeCategory } from "../../../client";

interface CategoryInputProps {
  categories: ItemBaseTypeCategory | ItemBaseTypeCategory[];
}

export const CategoryInput = ({ categories }: CategoryInputProps) => {
  if (!Array.isArray(categories)) {
    categories = [categories];
  }

  const { setItemCategory } = useGraphInputStore();

  const handleCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const itemCategory = event.target.value;
    setItemCategory(itemCategory);
  };

  let categoryOptions: JSX.Element[] = [];
  if (categories !== undefined) {
    categoryOptions = categories.map((baseCategory) => {
      return (
        <option
          value={baseCategory.category}
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
        key={"itemCategoryInput"}
      >
        <option
          value={undefined}
          key={"ItemCategoryInput" + "_option_" + "any"}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          Any
        </option>
        {categoryOptions}
      </Select>
    </Flex>
  );
};
