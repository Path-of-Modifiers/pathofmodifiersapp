import { Flex, VStack, Wrap, WrapItem, WrapProps } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInputComp/ModifierInput";
import { MiscItemInput } from "./MiscItemInput";
import { BaseInput } from "./BaseInput";
import { LeagueInput } from "./LeagueInput";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { ItemInput } from "./ItemInput";

// Graph Input Component  -  This component is used to input the query data.
export const GraphInput = (props: WrapProps) => {
    const expandedGraphInputFilters = useExpandedComponentStore(
        (state) => state.expandedGraphInputFilters
    );

    // Filters the available base type filters and modifiers, based on the chose item name
    // currently only works for uniques

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
                    </Flex>
                </WrapItem>
                <WrapItem>
                    <LeagueInput />
                </WrapItem>
                <WrapItem bg="ui.secondary">
                    <Flex
                        justifyContent={"space-between"}
                        flexWrap="wrap"
                        width={"bgBoxes.mediumPPBox"}
                        maxWidth="98vw"
                    >
                        <VStack spacing={2} mb={2}>
                            <BaseInput />
                            <MiscItemInput />
                        </VStack>
                        <ModifierInput />
                    </Flex>
                </WrapItem>
            </Wrap>
        )
    );
};
