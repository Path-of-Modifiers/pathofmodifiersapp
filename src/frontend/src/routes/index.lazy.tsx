import { createLazyFileRoute } from "@tanstack/react-router";
import SideBar from "../components/Common/Sidebar";
import Header from "../components/Common/Header";
import { Flex, Box } from "@chakra-ui/layout";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GraphInput } from "../components/Input/GraphInput";
// import { RenderPlot } from "../components/Graph/PlotlyGraph";
// import LineChart from "../components/Graph/PlotlyGraph";
import MyChart from "../components/Graph/test";

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

function Index() {
  return (
    <Flex direction="column" minHeight="100vh">
      <Header />
      <Flex flex="1" direction="row">
        <SideBar />
        <Flex flex="1" direction="row" p="1rem" bg="ui.main">
          <QueryClientProvider client={queryClient}>
            <GraphInput />
            {/* <MyChart/> */}
          </QueryClientProvider>
        </Flex>
      </Flex>
    </Flex>
  );
}
