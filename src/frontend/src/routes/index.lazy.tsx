import { createLazyFileRoute } from "@tanstack/react-router";
import SideBar from "../components/Common/Sidebar";
import Header from "../components/Common/Header";
import { Flex } from "@chakra-ui/layout";
import { ModifierInput } from "../components/Input/ModifierInput";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GetGroupedModifiersByEffect } from "../hooks/getGroupedModifiers";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

// Create a client
const queryClient = new QueryClient();

function Index() {
  const modifiersList = GetGroupedModifiersByEffect() as ModifierInput[];
  console.log(modifiersList)

  if (!modifiersList) {
    return "Error loading data. Please try again later.";
  }

  return (
    <Flex direction="column" minHeight="100vh">
      <Header />
      <Flex flex="1" direction="row">
        <SideBar />
        <Flex flex="1" direction="row" p="1rem" bg="ui.main">
          <QueryClientProvider client={queryClient}>
            <ModifierInput {...modifiersList} />
          </QueryClientProvider>
        </Flex>
      </Flex>
    </Flex>
  );
}
