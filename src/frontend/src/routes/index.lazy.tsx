import { createLazyFileRoute } from "@tanstack/react-router";
import SideBar from "../components/Common/Sidebar";
import Header from "../components/Common/Header";
import { Flex } from "@chakra-ui/layout";
import ModifierInput from "../components/Graph/ModifierInput";

export const Route = createLazyFileRoute("/")({
  component: Index,
});

function Index() {
  return (
    <Flex direction="column" minHeight="100vh">
      <Header />
      <Flex flex="1" direction="row">
        <SideBar />
        <Flex flex="1" direction="row" p="1rem" bg="ui.main">
          <ModifierInput/>
        </Flex>
      </Flex>
    </Flex>
  );
}
