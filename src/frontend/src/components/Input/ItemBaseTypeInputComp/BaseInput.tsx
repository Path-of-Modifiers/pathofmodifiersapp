import { Flex } from "@chakra-ui/layout";
import { useState } from "react";
import { Checkbox, CheckboxIcon, Text } from "@chakra-ui/react";
import { BaseTypeInput } from "./BaseTypeInput";
import { useQueryClient } from "@tanstack/react-query";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../../../client";
import { CategoryInput } from "./CategoryInput";
import { SubCategoryInput } from "./SubCategoryInput";
import { prefetchAllBaseTypeData } from "../../../hooks/getBaseTypeCategories";

// BaseInput component that contains the base type input, category input, and sub category input
export const BaseInput = () => {
  const [baseExpanded, setBaseExpanded] = useState(false);
  const [baseTypes, setBaseTypes] = useState<BaseType[]>([]);
  const [itemBaseTypeCategory, setItemBaseTypeCategory] = useState<
    ItemBaseTypeCategory[]
  >([]);
  const [itemBaseTypeSubCategory, setItemBaseTypeSubCategory] = useState<
    ItemBaseTypeSubCategory[]
  >([]);

  const queryClient = useQueryClient();

  const handleExpanded = () => {
    setBaseExpanded(!baseExpanded);
  };

  return (
    <Flex direction={"column"}>
      <Flex>
        <Checkbox
          onChange={handleExpanded}
          onMouseEnter={async () => {
            if (
              baseTypes.length === 0 &&
              itemBaseTypeCategory.length === 0 &&
              itemBaseTypeSubCategory.length === 0
            ) {
              // Prefetch base type data when hovering over the checkbox
              prefetchAllBaseTypeData(queryClient).then(
                (data) => {
                  setBaseTypes(data.baseTypes);
                  setItemBaseTypeCategory(data.itemBaseTypeCategory);
                  setItemBaseTypeSubCategory(data.itemBaseTypeSubCategory);
                },
                (error) => {
                  console.error(error);
                }
              );
            }
          }}
        >
          <CheckboxIcon />
        </Checkbox>
        <Text color={"ui.white"}>Base type</Text>
      </Flex>
      {baseExpanded &&
        baseTypes.length !== 0 &&
        itemBaseTypeCategory.length !== 0 &&
        itemBaseTypeSubCategory.length !== 0 && (
          <Flex flexWrap={"wrap"} width={650}>
            <BaseTypeInput baseTypes={baseTypes} />
            <CategoryInput categories={itemBaseTypeCategory} />
            <SubCategoryInput subCategories={itemBaseTypeSubCategory} />
          </Flex>
        )}
    </Flex>
  );
};
