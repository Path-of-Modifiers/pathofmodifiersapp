import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { GetItemBaseTypeSubCategories } from "../../../hooks/getBaseTypeCategories";
import { ItemBaseTypeSubCategory } from "../../../client";
import { capitalizeFirstLetter } from "../../../hooks/utils";

const handleCategoryChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  const itemSubCategory = event.target.value;
  useGraphInputStore.setState({ baseSpec: { subCategory: itemSubCategory } });
};

export const SubCategoryInput = () => {
  const subCategories: ItemBaseTypeSubCategory[] | undefined =
    GetItemBaseTypeSubCategories();

  let subCategoryOptions: JSX.Element[] = [];
  if (subCategories !== undefined) {
    subCategoryOptions = subCategories.map((subCategoryOption) => {
      return (
        <option
          value={capitalizeFirstLetter(subCategoryOption.subCategory)}
          key={"ItemCategoryInput" + "_option_" + subCategoryOption.subCategory}
          style={{ color: "white", backgroundColor: "#2d3333" }}
        >
          {capitalizeFirstLetter(subCategoryOption.subCategory)}
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
        {subCategoryOptions}
      </Select>
    </Flex>
  );
};
