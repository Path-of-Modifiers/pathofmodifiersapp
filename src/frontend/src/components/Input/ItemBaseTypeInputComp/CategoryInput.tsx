import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import { ItemBaseTypeCategory } from "../../../client";

interface CategoryInputProps {
  categories: ItemBaseTypeCategory | ItemBaseTypeCategory[];
}

// Category Input Component  -  This component is used to select the category of an item base type.
export const CategoryInput = ({ categories }: CategoryInputProps) => {
  if (!Array.isArray(categories)) {
    categories = [categories];
  }

  const defaultValue = undefined;

  const { setItemCategory } = useGraphInputStore();

  const getCategoryValue = () => {
    const category = useGraphInputStore.getState().baseSpec?.category;
    if (category) {
      return category;
    } else {
      return "";
    }
  };

  const handleCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const itemCategory = event.target.value;
    if (itemCategory === "Any") {
      setItemCategory(undefined);
    }
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
        value={getCategoryValue()}
        bgColor={"ui.input"}
        color={"ui.white"}
        onChange={(e) => handleCategoryChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"itemCategoryInput"}
      >
        <option
          value={defaultValue}
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
