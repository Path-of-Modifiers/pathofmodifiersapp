import { Box, Flex, Wrap, WrapItem } from "@chakra-ui/react";
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
      <Wrap>
        <WrapItem borderWidth={2} justifyContent={"center"} mr="auto" ml="auto">
          <Flex
            alignItems={"center"}
            justifyContent={"space-between"}
            width={"bgBoxes.mediumPPBox"}
          >
            <ItemInput />
            <LeagueInput />
          </Flex>
        </WrapItem>

        <WrapItem borderWidth={2} mr="auto" ml="auto">
          <Flex
            justifyContent={"space-between"}
            width={"bgBoxes.mediumPPBox"}
          >
            <Box width={"inputSizes.lgBox"} borderWidth={2}>
              <BaseInput />
              <MiscItemInput />
            </Box>
            <ModifierInput />
          </Flex>
        </WrapItem>
      </Wrap>
    )
  );
};
