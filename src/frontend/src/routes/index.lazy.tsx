import { createLazyFileRoute } from "@tanstack/react-router";
import Header from "../components/Common/Header";
import QueryButtons from "../components/Common/QueryButtons";
import { Flex, Box, VStack } from "@chakra-ui/layout";
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
        direction="row"
        bg="ui.main"
        opacity={0.98}
        justifyContent="center"
        width={"bgBoxes.defaultBox"}
        p={2}
        borderRadius={10}
        borderTopColor={"ui.darkBrown"}
        borderTopWidth={1}
        alignSelf="center"
      >
        <QueryClientProvider client={queryClient}>
          <VStack width="100%" >
            <GraphInput />
            <QueryButtons />
            <GraphComponent />
          </VStack>
        </QueryClientProvider>
      </Flex>
    </Flex>
  );
}
