import { Box, Button, ButtonGroup } from "@chakra-ui/react";
import { MdExpandMore, MdExpandLess } from "react-icons/md";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";

const QueryButtons = () => {
  const { setExpandedGraphInputFilters } = useExpandedComponentStore();

  const filterExpanded = useExpandedComponentStore(
    (state) => state.expandedGraphInputFilters
  );

  const handleShowingFilter = () => {
    setExpandedGraphInputFilters(!filterExpanded);
  };

  return (
    <Box bg="ui.main">
      <ButtonGroup variant="solid" colorScheme="red">
        <Button>Clear Query</Button>
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
