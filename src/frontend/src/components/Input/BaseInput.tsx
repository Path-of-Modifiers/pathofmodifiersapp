import { Flex } from "@chakra-ui/layout";
import { useEffect } from "react";
import { BaseTypeInput } from "./ItemBaseTypeInputComp/BaseTypeInput";
import { ItemBaseType } from "../../client";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { AddICheckText } from "../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";

interface BaseInputProps {
  itemBaseTypes: ItemBaseType[];
}

// BaseInput component that contains the base type input, category input, and sub category input
export const BaseInput = (props: BaseInputProps) => {
  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const { expandedBaseType, setExpandedBaseType } = useExpandedComponentStore();

  const handleExpanded = () => {
    setExpandedBaseType(!expandedBaseType);
  };

  useEffect(() => {
    if (clearClicked) {
      setExpandedBaseType(false);
    }
  }, [clearClicked, setExpandedBaseType]);

  const baseTypes = props.itemBaseTypes.map(
    (itemBaseType) => itemBaseType.baseType
  );
  const nonUniqueCategories = props.itemBaseTypes.map(
    (itemBaseType) => itemBaseType.category
  );
  const categories = [...new Set(nonUniqueCategories)];
  const nonUniqueSubCategories = props.itemBaseTypes
    .map((itemBaseType) => itemBaseType.subCategory)
    .filter((subCategory) => subCategory != null);
  const subCategories = [...new Set(nonUniqueSubCategories)];

  return (
    <Flex direction={"column"} width={"inputSizes.lgBox"}>
      <AddICheckText
        isChecked={expandedBaseType}
        onChange={handleExpanded}
        text="Base Type"
      />
      {expandedBaseType && props.itemBaseTypes.length !== 0 && (
        <Flex flexWrap={"wrap"} justifyContent={"flex-start"} ml={10} gap={2}>
          <BaseTypeInput baseTypes={baseTypes} />
          <CategoryInput categories={categories} />
          <SubCategoryInput subCategories={subCategories} />
        </Flex>
      )}
    </Flex>
  );
};
