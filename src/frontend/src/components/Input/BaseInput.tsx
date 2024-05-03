import { Flex } from "@chakra-ui/layout";
import { useState } from "react";
import { Checkbox, CheckboxIcon, Text } from "@chakra-ui/react";
import { BaseTypeInput } from "./ItemBaseTypeInputComp/BaseTypeInput";
import { useQueryClient } from "@tanstack/react-query";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
  ItemBaseTypesService,
} from "../../client";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";
import React from "react";

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

  const prefetchAllBaseTypeData = async () => {
    await queryClient.prefetchQuery({
      queryKey: ["baseTypes"],
      queryFn: async () => {
        const data =
          await ItemBaseTypesService.getBaseTypesApiApiV1ItemBaseTypeBaseTypesGet();
        if (Array.isArray(data)) {
          setBaseTypes(data);
        } else {
          setBaseTypes([data]);
        }
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    await queryClient.prefetchQuery({
      queryKey: ["itemBaseTypeCategory"],
      queryFn: async () => {
        const data =
          await ItemBaseTypesService.getUniqueCategoriesApiApiV1ItemBaseTypeUniqueCategoriesGet();
        if (Array.isArray(data)) {
          setItemBaseTypeCategory(data);
        } else {
          setItemBaseTypeCategory([data]);
        }
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    await queryClient.prefetchQuery({
      queryKey: ["itemBaseTypeSubCategory"],
      queryFn: async () => {
        const data =
          await ItemBaseTypesService.getUniqueSubCategoriesApiApiV1ItemBaseTypeUniqueSubCategoriesGet();
        if (Array.isArray(data)) {
          setItemBaseTypeSubCategory(data);
        } else {
          setItemBaseTypeSubCategory([data]);
        }
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    setTimeout(() => {
      rerender(0);
    }, 1);
  };
  return (
    <Flex direction={"column"}>
      <Flex>
        <Checkbox
          onChange={handleExpanded}
          onMouseEnter={async () => {
            prefetchAllBaseTypeData();
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
