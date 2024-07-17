import { Box, Button, Flex, FlexProps } from "@chakra-ui/react";
import { MdExpandMore, MdExpandLess } from "react-icons/md";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { useGraphInputStore } from "../../store/GraphInputStore";
import {
  checkGraphQueryLeageInput,
  checkGraphQueryModifierInput,
} from "../../hooks/graphing/checkGraphQueryInput";
import { useErrorStore } from "../../store/ErrorStore";

const QueryButtons = (props: FlexProps) => {
  const { setExpandedGraphInputFilters } = useExpandedComponentStore();
  const { setResultError } = useErrorStore();
  const { setPlotQuery } = useGraphInputStore();

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
    setResultError(false);
    setPlotQuery();
    const leagueValid = checkGraphQueryLeageInput();
    const modifierValid = checkGraphQueryModifierInput();
    if (leagueValid && modifierValid) {
      useGraphInputStore.getState().setQueryClicked();

      // This is a hack to make sure the clearClicked is set to false after the
      // state is updated.
      setTimeout(() => {
        useGraphInputStore.getState().queryClicked = false;
      }, 20);
    }
  };
  return (
    <Flex
      {...props}
      direction={["column", "row"]} // Column for small screens, row for larger screens
      alignItems="center"
      width="100%"
      flexWrap="wrap"
    >
      <Box flex={["none", "1"]} mb={[4, 0]}></Box>{" "}
      {/* Empty space for centering the middle item */}
      <Box textAlign="center" mb={[4, 0]}>
        <Button
          variant="solid"
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          borderWidth={1}
          borderColor="ui.grey"
          width="inputSizes.lgBox"
          maxW="100vw"
          onClick={handlePlotQuery}
        >
          Query and Plot
        </Button>
      </Box>
      <Flex
        flex={["none", "1"]}
        justifyContent={["center", "flex-end"]}
        width={["100%", "auto"]} // Full width for small screens, auto for larger screens
      >
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
          rightIcon={filterExpanded ? <MdExpandLess /> : <MdExpandMore />}
          onClick={handleShowingFilter}
        >
          {filterExpanded ? "Hide Filters" : "Show Filters"}
        </Button>
      </Flex>
    </Flex>
  );
};

export default QueryButtons;
