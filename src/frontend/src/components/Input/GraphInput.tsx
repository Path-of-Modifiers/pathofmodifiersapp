import { Flex, VStack, Wrap, WrapItem, WrapProps } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInputComp/ModifierInput";
import { MiscItemInput } from "./MiscItemInput";
import { BaseInput } from "./BaseInput";
import { LeagueInput } from "./LeagueInput";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { ItemInput } from "./ItemInput";
import {
  BaseType,
  GroupedModifierByEffect,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../../client";

interface GraphInputProps extends WrapProps {
  prefetchedmodifiers: GroupedModifierByEffect[];
  prefetchbasetypes: BaseType[];
  prefetchcategories: ItemBaseTypeCategory[];
  prefetchsubcategories: ItemBaseTypeSubCategory[];
}

// Graph Input Component  -  This component is used to input the query data.
export const GraphInput = (props: GraphInputProps) => {
  const expandedGraphInputFilters = useExpandedComponentStore(
    (state) => state.expandedGraphInputFilters
  );

  return (
    expandedGraphInputFilters && (
      <Wrap {...props}>
        <WrapItem justifyContent={"center"} mr="auto" ml="auto">
          <Flex
            alignItems={"center"}
            justifyContent={"space-between"}
            gap={2}
            width={"bgBoxes.mediumPPBox"}
          >
            <ItemInput />
            <LeagueInput />
          </Flex>
        </WrapItem>

        <WrapItem mr="auto" ml="auto">
          <Flex justifyContent={"space-between"} width={"bgBoxes.mediumPPBox"}>
            <VStack spacing={2} align={"flex-start"} width={"inputSizes.lgBox"}>
              <BaseInput
                baseTypes={props.prefetchbasetypes}
                categories={props.prefetchcategories}
                subCategories={props.prefetchsubcategories}
              />
              <MiscItemInput />
            </VStack>
            <ModifierInput prefetchedmodifiers={props.prefetchedmodifiers} />
          </Flex>
        </WrapItem>
      </Wrap>
    )
  );
};
