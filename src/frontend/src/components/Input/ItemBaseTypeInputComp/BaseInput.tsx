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
import React from "react";
import { prefetchAllBaseTypeData } from "../../../hooks/getBaseTypeCategories";

export const BaseInput = () => {
  const [baseExpanded, setBaseExpanded] = useState(false);
  const [baseTypes, setBaseTypes] = useState<BaseType[]>([]);
  const [itemBaseTypeCategory, setItemBaseTypeCategory] = useState<
    ItemBaseTypeCategory[]
  >([]);
  const [itemBaseTypeSubCategory, setItemBaseTypeSubCategory] = useState<
    ItemBaseTypeSubCategory[]
  >([]);
  const rerender = React.useState(0)[1];

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
              prefetchAllBaseTypeData(queryClient).then(
                (data) => {
                  setBaseTypes(data.baseTypes);
                  setItemBaseTypeCategory(data.itemBaseTypeCategory);
                  setItemBaseTypeSubCategory(data.itemBaseTypeSubCategory);
                  rerender((prev) => prev + 1);
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
