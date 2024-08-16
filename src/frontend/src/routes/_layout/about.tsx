import { createFileRoute } from "@tanstack/react-router";
import { Flex, Box, VStack, Text } from "@chakra-ui/layout";

import Header from "../../components/Common/Header";
import Footer from "../..//components/Common/Footer";
import { TextWithUnderline } from "../../components/Text/TextWithUnderline";

export const Route = createFileRoute("/_layout/about")({
  component: About,
});

// About Route  - This component is the main component for the about route.
function About() {
  const aboutDescription = `This website uses public stash data to track item prices and their modifiers. The data is shown in graphs for easy understanding of pricing trends.

Supported items are listed under the "Item Name" field. As of now, we support a limited number of unique items. We plan to add more items and modifiers in the future.

The data is updated live with a 5 minute delay. The data is fetched from the official Path of Exile API. Some techniques are used to prevent price manipulation by users.
  `;
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
        color="ui.white"
      >
        <VStack width="100%" align="left">
          <Box width="100%">
            <TextWithUnderline
              text="Data Analysis Tool for POE Item Prices and Modifiers"
              textProps={{ fontSize: "2xl", marginBottom: "1rem" }}
            />
            <Text whiteSpace="pre-line">{aboutDescription}</Text>
          </Box>
          <Footer />
        </VStack>
      </Flex>
    </Flex>
  );
}
