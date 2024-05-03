import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import { ItemBaseTypeSubCategory } from "../../../client";

interface SubCategoryInputProps {
  subCategories: ItemBaseTypeSubCategory | ItemBaseTypeSubCategory[];
}

export const SubCategoryInput = ({ subCategories }: SubCategoryInputProps) => {
  if (!Array.isArray(subCategories)) {
    subCategories = [subCategories];
  }

  const { setItemSubCategory } = useGraphInputStore();

  const handleSubCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const itemSubCategory = event.target.value;
    setItemSubCategory(itemSubCategory);
  };

  let categoryOptions: JSX.Element[] = [];
  if (subCategories !== undefined) {
    categoryOptions = subCategories.map((baseCategory) => {
      return (
        <option
          value={capitalizeFirstLetter(baseCategory.subCategory)}
          key={"ItemSubCategoryInput" + "_option_" + baseCategory.subCategory}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          {capitalizeFirstLetter(baseCategory.subCategory)}
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
        onChange={(e) => handleSubCategoryChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"itemSubCategoryInput"}
      >
        {categoryOptions}
      </Select>
    </Flex>
  );
};
