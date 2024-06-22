import { Flex } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInputComp/ModifierInput";
import { MiscItemInput } from "./MiscItemInput";
import { BaseInput } from "./BaseInput";
import { LeagueInput } from "./LeagueInput";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { ItemInput } from "./ItemInput";

// Graph Input Component  -  This component is used to input the query data.
export const GraphInput = () => {
  const expandedGraphInputFilters = useExpandedComponentStore(
    (state) => state.expandedGraphInputFilters
  );

  return (
    expandedGraphInputFilters && (
      <Flex flexWrap="wrap" direction="row" alignItems="center" width={300}>
        <LeagueInput />
        <ItemInput />
        <BaseInput />
        <MiscItemInput />
        <ModifierInput />
      </Flex>
    )
  );
};
