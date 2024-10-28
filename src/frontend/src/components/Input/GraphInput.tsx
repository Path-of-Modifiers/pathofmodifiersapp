import { Flex, VStack, Wrap, WrapItem, WrapProps } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInputComp/ModifierInput";
import { MiscItemInput } from "./MiscItemInput";
import { BaseInput } from "./BaseInput";
import { LeagueInput } from "./LeagueInput";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { ItemInput } from "./ItemInput";
import { GroupedModifierByEffect, ItemBaseType } from "../../client";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect, useState } from "react";

interface GraphInputProps extends WrapProps {
  prefetchedmodifiers: GroupedModifierByEffect[];
  prefetcheditembasetypes: ItemBaseType[];
  prefecteditemnames: string[];
}

// Graph Input Component  -  This component is used to input the query data.
export const GraphInput = (props: GraphInputProps) => {
  const expandedGraphInputFilters = useExpandedComponentStore(
    (state) => state.expandedGraphInputFilters
  );
  const { itemName } = useGraphInputStore();

  const { prefetchedmodifiers, prefetcheditembasetypes, prefecteditemnames } =
    props;

  const [modifiers, setModifiers] =
    useState<GroupedModifierByEffect[]>(prefetchedmodifiers);
  const [itemBaseTypes, setItemBaseTypes] = useState<ItemBaseType[]>(
    prefetcheditembasetypes
  );

  // Filters the available base type filters and modifiers, based on the chose item name
  // currently only works for uniques
  useEffect(() => {
    if (itemName === undefined) {
      setModifiers(prefetchedmodifiers);
      setItemBaseTypes(prefetcheditembasetypes);
    } else {
      setModifiers(
        prefetchedmodifiers.filter((modifier) =>
          modifier.relatedUniques?.includes(itemName)
        )
      );
      setItemBaseTypes(
        prefetcheditembasetypes.filter((itemBaseType) =>
          itemBaseType.relatedUniques?.includes(itemName)
        )
      );
    }
  }, [itemName, prefetchedmodifiers, prefetcheditembasetypes]);

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
            <ItemInput itemNameInputProps={{ uniques: prefecteditemnames }} />
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
              <BaseInput itemBaseTypes={itemBaseTypes} />
              <MiscItemInput />
            </VStack>
            <ModifierInput prefetchedmodifiers={modifiers} />
          </Flex>
        </WrapItem>
      </Wrap>
    )
  );
};
