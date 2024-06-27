import { Flex } from "@chakra-ui/layout";
import { useEffect } from "react";
import { BaseTypeInput } from "./ItemBaseTypeInputComp/BaseTypeInput";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../../client";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { AddICheckText } from "../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";

interface BaseInputProps {
  baseTypes: BaseType[];
  categories: ItemBaseTypeCategory[];
  subCategories: ItemBaseTypeSubCategory[];
}

// BaseInput component that contains the base type input, category input, and sub category input
export const BaseInput = (props: BaseInputProps) => {
  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const baseTypeExpanded = useExpandedComponentStore(
    (state) => state.expandedBaseType
  );

  const { setExpandedBaseType } = useExpandedComponentStore();

  const handleExpanded = () => {
    setExpandedBaseType(!baseTypeExpanded);
  };

  useEffect(() => {
    if (clearClicked) {
      setExpandedBaseType(false);
    }
  }, [clearClicked, setExpandedBaseType]);

  return (
    <Flex direction={"column"} width={"inputSizes.lgBox"}>
      <AddICheckText
        isChecked={baseTypeExpanded}
        onChange={handleExpanded}
        text="Base type"
      />
      {baseTypeExpanded &&
        props.baseTypes.length !== 0 &&
        props.categories.length !== 0 &&
        props.subCategories.length !== 0 && (
          <Flex flexWrap={"wrap"} justifyContent={"flex-start"} ml={10} gap={2}>
            <BaseTypeInput baseTypes={props.baseTypes} />
            <CategoryInput categories={props.categories} />
            <SubCategoryInput subCategories={props.subCategories} />
          </Flex>
        )}
    </Flex>
  );
};
