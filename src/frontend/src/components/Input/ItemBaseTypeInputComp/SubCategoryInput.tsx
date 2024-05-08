import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import { ItemBaseTypeSubCategory } from "../../../client";

interface SubCategoryInputProps {
  subCategories: ItemBaseTypeSubCategory | ItemBaseTypeSubCategory[];
}

// Sub Category Input Component  -  This component is used to select the sub category of an item base type.
export const SubCategoryInput = ({ subCategories }: SubCategoryInputProps) => {
  if (!Array.isArray(subCategories)) {
    subCategories = [subCategories];
  }

  const defaultValue = undefined;

  const getSubCategoryValue = () => {
    const baseType = useGraphInputStore.getState().baseSpec?.subCategory;
    if (baseType) {
      return baseType;
    } else {
      return "";
    }
  };

  const { setItemSubCategory } = useGraphInputStore();

  const handleSubCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const itemSubCategory = event.target.value;
    if (itemSubCategory === "Any") {
      setItemSubCategory(undefined);
    }
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
        Item Sub Category
      </Text>
      <Select
        value={getSubCategoryValue()}
        bgColor={"ui.input"}
        color={"ui.white"}
        onChange={(e) => handleSubCategoryChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"itemSubCategoryInput"}
      >
        <option
          value={defaultValue}
          key={"ItemSubCategoryInput" + "_option_" + "any"}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          Any
        </option>
        {categoryOptions}
      </Select>
    </Flex>
  );
};
