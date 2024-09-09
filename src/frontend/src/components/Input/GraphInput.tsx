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
        <WrapItem>
          <Flex
            justifyContent={"space-between"}
            flexWrap="wrap"
            gap={2}
            width={"bgBoxes.mediumPPBox"}
            maxWidth="98vw"
          >
            <ItemInput />
            <LeagueInput />
          </Flex>
        </WrapItem>

        <WrapItem bg="ui.secondary">
          <Flex
            justifyContent={"space-between"}
            flexWrap="wrap"
            width={"bgBoxes.mediumPPBox"}
            maxWidth="98vw"
          >
            <VStack spacing={2} mb={2}>
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
