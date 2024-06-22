import { createLazyFileRoute } from "@tanstack/react-router";
import Header from "../components/Common/Header";
import QueryButtons from "../components/Common/QueryButtons";
import { Flex, Box } from "@chakra-ui/layout";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GraphInput } from "../components/Input/GraphInput";
import GraphComponent from "../components/Graph/GraphComponent";
import img from "../assets/wallpap_castle_high_res.jpeg";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity,
    },
  },
});

// Index Component  -  This component is the main component for the index route.
function Index() {
  return (
    <Flex direction="column" minHeight="100vh" bgImage={img} bgSize="cover">
      <Box mb={"7rem"}>
        <Header />
      </Box>

      <Flex
        flex="1"
        direction="row"
        width="bgBoxes.defaultBox"
        mr="auto"
        ml="auto"
      >
        <Flex
          flex="1"
          direction="column"
          p="3rem"
          bg="ui.main"
          opacity={0.98}
          borderRadius={10}
          borderTopColor={"ui.darkBrown"}
          borderTopWidth={1}
        >
          <QueryClientProvider client={queryClient}>
            <Box>
              <GraphInput />
              <QueryButtons />
              <GraphComponent />
            </Box>
          </QueryClientProvider>
        </Flex>
      </Flex>
    </Flex>
  );
}
