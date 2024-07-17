import { createLazyFileRoute } from "@tanstack/react-router";
import { Flex, Box, VStack } from "@chakra-ui/layout";

import Header from "../components/Common/Header";
import Footer from "../components/Common/Footer";
import { TextWithUnderline } from "../components/Text/TextWithUnderline";

export const Route = createLazyFileRoute("/about")({
  component: About,
});

// Index Component  -  This component is the main component for the index route.
function About() {
  return (
    <Flex direction="column" minHeight="100vh" minWidth="98vw" bg="ui.main">
      <Box mb={"7rem"}>
        <Header />
      </Box>

      <Flex
        direction="row"
        bg="ui.secondary"
        opacity={0.98}
        height="100vh"
        width={"bgBoxes.defaultBox"}
        maxWidth={"98vw"}
        p={2}
        borderTopRadius={10}
        borderTopColor={"ui.darkBrown"}
        borderTopWidth={1}
        alignSelf="center"
      >
        <VStack width="100%">
          <Box width="48%">
            <TextWithUnderline text="About" />
          </Box>
          <Footer />
        </VStack>
      </Flex>
    </Flex>
  );
}
