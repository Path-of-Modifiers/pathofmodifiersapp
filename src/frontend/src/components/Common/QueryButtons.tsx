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

  return (
    <Box bg="ui.main">
      <ButtonGroup variant="solid" colorScheme="red">
        <Button onClick={handleClearQuery}>Clear Query</Button>
        <Button variant="solid" colorScheme="green">
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
