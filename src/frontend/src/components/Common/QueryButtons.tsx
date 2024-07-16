import { Box, Button, ButtonGroup } from "@chakra-ui/react";
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
    <Box bg="ui.main">
      <ButtonGroup>
        <Button variant="solid" colorScheme="red" onClick={handleClearQuery}>
          Clear Query
        </Button>
        <Button variant="solid" colorScheme="green" onClick={handlePlotQuery}>
          Query and Plot
        </Button>
        <Button
          variant="solid"
          colorScheme="gray"
          rightIcon={filterExpanded ? <MdExpandLess /> : <MdExpandMore />}
          onClick={handleShowingFilter}
        >
          {filterExpanded ? "Hide Filters" : "Show Filters"}
        </Button>
      </ButtonGroup>
    </Box>
  );
};

export default QueryButtons;
