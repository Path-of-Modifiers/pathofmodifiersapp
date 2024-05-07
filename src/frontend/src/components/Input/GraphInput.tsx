import { Box } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInputComp/ModifierInput";
import { MiscItemInput } from "./ItemInputComp/MiscItemInput";
import { BaseInput } from "./ItemBaseTypeInputComp/BaseInput";
import { IsItemInput } from "./ItemInputComp/IsItemProp";
import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";
import { LeagueInput } from "./LeagueInput";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";

export const GraphInput = () => {
  const expandedGraphInputFilters = useExpandedComponentStore(
    (state) => state.expandedGraphInputFilters
  );

  return (
    expandedGraphInputFilters && (
      <Box p={5}>
        <LeagueInput />
        <ItemNameInput />
        <ItemRarityInput />
        <IsItemInput
          itemSpecKey={"identified"}
          text={"Identified"}
        />
        <BaseInput />
        <MiscItemInput />
        <ModifierInput />
      </Box>
    )
  );
};
