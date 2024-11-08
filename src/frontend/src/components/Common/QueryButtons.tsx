import { Box, Button, Flex, FlexProps } from "@chakra-ui/react";
import { MdExpandMore, MdExpandLess } from "react-icons/md";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { useGraphInputStore } from "../../store/GraphInputStore";
import {
    checkGraphQueryLeageInput,
    checkGraphQueryModifierInput,
} from "../../hooks/graphing/checkGraphQueryInput";
import { useErrorStore } from "../../store/ErrorStore";
import { ErrorMessage } from "../../components/Input/StandardLayoutInput/ErrorMessage";
import { getOptimizedPlotQuery } from "../../hooks/graphing/utils";

const QueryButtons = (props: FlexProps) => {
    const { setExpandedGraphInputFilters } = useExpandedComponentStore();
    const {
        modifiersError,
        leagueError,
        resultError,
        noRelatedUniqueError,
        itemDoesNotHaveSelectedModifiersError,
        baseSpecDoesNotMatchError,
        setResultError,
    } = useErrorStore();
    const { stateHash, fetchStatus, setHashFromStore, setPlotQuery } =
        useGraphInputStore();
    const isFetching = fetchStatus === "fetching";

    const filterExpanded = useExpandedComponentStore(
        (state) => state.expandedGraphInputFilters
    );

    const handleShowingFilter = () => {
        setExpandedGraphInputFilters(!filterExpanded);
    };

    const handleClearQuery = () => {
        useGraphInputStore.getState().setClearClicked();

        // This is a hack to make sure the clearClicked is set to false after the
        // state is updated.
        setTimeout(() => {
            useGraphInputStore.getState().clearClicked = false;
        }, 10);
    };

    const handlePlotQuery = () => {
        if (isFetching) return;
        if (stateHash) return;
        setHashFromStore();
        setResultError(false);
        const plotQuery = getOptimizedPlotQuery();
        if (plotQuery === undefined) return;
        setPlotQuery(plotQuery);
        const leagueValid = checkGraphQueryLeageInput();
        const modifierValid = checkGraphQueryModifierInput();
        if (leagueValid && modifierValid) {
            useGraphInputStore.getState().setQueryClicked();

            // This is a hack to make sure the clearClicked is set to false after the
            // state is updated.
            setTimeout(() => {
                useGraphInputStore.getState().queryClicked = false;
                useGraphInputStore.getState().stateHash = undefined;
            }, 20);
        }
    };
    return (
        <Flex
            {...props}
            direction={["column", "row"]} // Column for small screens, row for larger screens
            alignItems="center"
            width="bgBoxes.defaultBox"
            maxW="98vw"
            flexWrap="wrap"
        >
            <Box
                width="10vw"
                flex={["none", "1"]}
                mb={[4, 20]}
                alignContent={"center"}
            />
            {/* Empty space for centering the middle item */}
            <Box textAlign="center" mb={[4, 0]}>
                <Button
                    variant="solid"
                    bg="ui.queryBaseInput"
                    color="ui.white"
                    _hover={{
                        bg: isFetching
                            ? "ui.queryBaseInput"
                            : "ui.queryMainInput",
                    }}
                    borderWidth={1}
                    borderColor="ui.grey"
                    width={["inputSizes.defaultBox", "inputSizes.lgBox"]}
                    maxW="98vw"
                    onClick={handlePlotQuery}
                    disabled={isFetching}
                    opacity={isFetching ? 0.5 : 1}
                    cursor={isFetching ? "not-allowed" : "pointer"}
                >
                    Query and Plot
                </Button>
            </Box>
            <Flex flex={["none", "1"]} justifyContent={["center", "flex-end"]}>
                <Button
                    variant="solid"
                    bg="ui.input"
                    color="ui.white"
                    _hover={{ bg: "ui.lightInput" }}
                    onClick={handleClearQuery}
                    borderWidth={1}
                    borderColor="ui.grey"
                    mb={[2, 0]}
                >
                    Clear Query
                </Button>
                <Button
                    variant="solid"
                    bg="ui.queryBaseInput"
                    color="ui.white"
                    _hover={{ bg: "ui.queryMainInput" }}
                    borderWidth={1}
                    ml={[0, 2]}
                    borderColor="ui.grey"
                    rightIcon={
                        filterExpanded ? <MdExpandLess /> : <MdExpandMore />
                    }
                    onClick={handleShowingFilter}
                >
                    {filterExpanded ? "Hide Filters" : "Show Filters"}
                </Button>
            </Flex>

            {modifiersError && !noRelatedUniqueError && (
                <ErrorMessage
                    alertTitle="No Modifiers Selected"
                    alertDescription="Please select at least one modifier."
                />
            )}
            {leagueError && (
                <ErrorMessage
                    alertTitle="No League Selected"
                    alertDescription="Please select a league."
                />
            )}
            {resultError && (
                <ErrorMessage
                    alertTitle="No Results Found"
                    alertDescription="No results were found for the current query."
                />
            )}
            {noRelatedUniqueError && (
                <ErrorMessage
                    alertTitle="No query performed"
                    alertDescription="The modifiers you have chosen cannot appear on the same Unique."
                />
            )}
            {itemDoesNotHaveSelectedModifiersError && (
                <ErrorMessage
                    alertTitle="No query performed"
                    alertDescription="The chosen unique cannot have the currently selected modifiers."
                />
            )}
            {baseSpecDoesNotMatchError && (
                <ErrorMessage
                    alertTitle="No query performed"
                    alertDescription="The chosen base type filter cannot have the currently selected modifiers."
                />
            )}
        </Flex>
    );
};

export default QueryButtons;
