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
    useExpandedComponentStore.getState().setExpandedGraphInputFilters(false);
    useGraphInputStore.getState().setPlotQuery();
    useGraphInputStore.getState().setQueryClicked();

    // This is a hack to make sure the clearClicked is set to false after the
    // state is updated.
    setTimeout(() => {
      useGraphInputStore.getState().queryClicked = false;
    }, 20);
  };

  return (
    <Flex width={"100%"} justifyContent={"end"}>
      <Box>
        {" "}
        <Button
          variant="solid"
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          _focus={{ bg: "ui.queryMainInput" }}
          borderWidth={1}
          borderColor={"ui.grey"}
          width={"inputSizes.lgBox"}
          onClick={handlePlotQuery}
        >
          Query and Plot
        </Button>
      </Box>
      <Flex width="585px" justifyContent={"end"} gap={2} mr={2}>
        <Button
          variant="solid"
          bg="ui.input"
          color="ui.white"
          _hover={{ bg: "ui.lightInput" }}
          _focus={{ bg: "ui.lightInput" }}
          onClick={handleClearQuery}
          borderWidth={1}
          borderColor={"ui.grey"}
        >
          Clear Query
        </Button>
        <Button
          variant="solid"
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          _focus={{ bg: "ui.queryMainInput" }}
          borderWidth={1}
          borderColor={"ui.grey"}
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
