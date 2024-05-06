import { createLazyFileRoute } from "@tanstack/react-router";
import SideBar from "../components/Common/Sidebar";
import Header from "../components/Common/Header";
import QueryButtons from "../components/Common/QueryButtons";
import { Flex } from "@chakra-ui/layout";
import { Query, QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GraphInput } from "../components/Input/GraphInput";

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
      <QueryButtons />
      <Flex flex="1" direction="row">
        <SideBar />
        <Flex flex="1" direction="row" p="1rem" bg="ui.main">
          <QueryClientProvider client={queryClient}>
            <GraphInput />
          </QueryClientProvider>
        </Flex>
      </Flex>
    </Flex>
  );
}
