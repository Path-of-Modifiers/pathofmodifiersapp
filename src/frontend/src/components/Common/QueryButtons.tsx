import { Box, Button, Flex } from "@chakra-ui/react";
import { MdExpandMore, MdExpandLess } from "react-icons/md";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";
import { useGraphInputStore } from "../../store/GraphInputStore";

const QueryButtons = () => {
  const { setExpandedGraphInputFilters } = useExpandedComponentStore();

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
    useGraphInputStore.getState().setPlotQuery();
    useGraphInputStore.getState().setQueryClicked();

    // This is a hack to make sure the clearClicked is set to false after the
    // state is updated.
    setTimeout(() => {
      useGraphInputStore.getState().queryClicked = false;
    }, 20);
  };

  return (
    <Flex bg="ui.main" p={2} justifyContent="center">
      <Button variant="solid" colorScheme="green" onClick={handlePlotQuery} mr="auto" ml="auto">
        Query and Plot
      </Button>

      <Box>
        <Button variant="solid" colorScheme="red" onClick={handleClearQuery} mr={4}>
          Clear Query
        </Button>

        <Button
          variant="solid"
          colorScheme="gray"
          rightIcon={filterExpanded ? <MdExpandLess /> : <MdExpandMore />}
          onClick={handleShowingFilter}
          alignSelf={"right"}
        >
          {filterExpanded ? "Hide Filters" : "Show Filters"}
        </Button>
      </Box>
    </Flex>
  );
};

export default QueryButtons;
