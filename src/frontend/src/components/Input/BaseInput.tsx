import { Box, Flex } from "@chakra-ui/layout";
import { useEffect, useState } from "react";
import { Text } from "@chakra-ui/react";
import { BaseTypeInput } from "./ItemBaseTypeInputComp/BaseTypeInput";
import { useQueryClient } from "@tanstack/react-query";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../../client";
import { CategoryInput } from "./ItemBaseTypeInputComp/CategoryInput";
import { SubCategoryInput } from "./ItemBaseTypeInputComp/SubCategoryInput";
import { prefetchAllBaseTypeData } from "../../hooks/getBaseTypeCategories";
import { useGraphInputStore } from "../../store/GraphInputStore";
import AddIconCheckbox from "../Icon/AddIconCheckbox";

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

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const queryClient = useQueryClient();

  const handleExpanded = () => {
    setBaseExpanded(!baseExpanded);
  };

  useEffect(() => {
    if (clearClicked) {
      setBaseExpanded(false);
    }
  }, [clearClicked]);

  return (
    <Flex direction={"column"} width={"inputSizes.lgBox"}>
      <Flex alignItems={"center"} gap={2}>
        <AddIconCheckbox
          isChecked={baseExpanded}
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
        ></AddIconCheckbox>
        <Box flex="1" position="relative">
          <Text color="ui.white">Base type</Text>
          <Box
            position="absolute"
            top="2"
            bottom="0"
            left="0"
            right="0"
            borderBottom="1px solid"
            borderColor="ui.grey"
          />
        </Box>
      </Flex>
      {baseExpanded &&
        baseTypes.length !== 0 &&
        itemBaseTypeCategory.length !== 0 &&
        itemBaseTypeSubCategory.length !== 0 && (
          <Flex flexWrap={"wrap"} justifyContent={"flex-start"} ml={6} gap={2}>
            <BaseTypeInput baseTypes={baseTypes} />
            <CategoryInput categories={itemBaseTypeCategory} />
            <SubCategoryInput subCategories={itemBaseTypeSubCategory} />
          </Flex>
        )}
    </Flex>
  );
};
