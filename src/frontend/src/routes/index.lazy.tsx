import { createLazyFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import SideBar from "../components/Common/Sidebar";
import Header from "../components/Common/Header";
import QueryButtons from "../components/Common/QueryButtons";
import { Flex } from "@chakra-ui/layout";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GraphInput } from "../components/Input/GraphInput";
// import { RenderPlot } from "../components/Graph/PlotlyGraph";
// import LineChart from "../components/Graph/PlotlyGraph";
import GraphComponent from "../components/Graph/GraphComponent";
import testAPI from "../hooks/graphing/processPlottingData";

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
  const [showingFilter, setShowingFilter] = useState(true);
  return (
    <Flex direction="column" minHeight="100vh">
      <Header />
      <QueryButtons showingFilter={showingFilter} setShowingFilter={setShowingFilter}/>
      <Flex flex="1" direction="row">
        {/* <SideBar /> */}
        <Flex flex="1" direction="column" p="1rem" bg="ui.main">
          <QueryClientProvider client={queryClient}>
            <GraphInput showingFilter={showingFilter}/>
            <GraphComponent/>
          </QueryClientProvider>
        </Flex>
      </Flex>
    </Flex>
  );
}
