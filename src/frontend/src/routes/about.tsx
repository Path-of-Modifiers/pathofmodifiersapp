import { createFileRoute, Link as RouterLink } from "@tanstack/react-router";
import { Flex, Box, VStack, Text, Link } from "@chakra-ui/layout";

import Footer from "../components/Common/Footer";

export const Route = createFileRoute("/about")({
  component: About,
});

// About Route  - This component is the main component for the about route.
function About() {
  const aboutDescription = `This website uses public stash data to track item prices and their modifiers. The data is shown in graphs for easy understanding of pricing trends.

Supported items are listed under the "Item Name" field. As of now, we support a limited number of unique items. We plan to add more items and modifiers in the future.

The data is updated live with a 5 minute delay. The data is fetched from the official Path of Exile API. Some techniques are used to prevent price manipulation by users.
  `;

  return (
    <Flex
      direction="column"
      bg="ui.main"
      width="99vw"
      minWidth="bgBoxes.miniPBox"
      alignItems="center"
      color="ui.white"
    >
      <Box width="full" padding="1rem">
        <Link
          color="ui.white"
          fontSize="30px"
          fontWeight="medium"
          as={RouterLink}
          to="/"
          from="about"
          key={(Math.random() + 1).toString(36).substring(7)} // Forces reload to make login work
          _hover={{
            color: "ui.inputChanged",
            textDecoration: "underline",
          }}
        >
          Path of Modifiers
        </Link>
      </Box>
      <Flex
        direction="column"
        bg="ui.main"
        width="99vw"
        minWidth="bgBoxes.miniPBox"
      >
        <Text alignSelf="center" fontSize={50} mb="2rem">
          About Path of Modifiers
        </Text>
        <Flex
          direction="row"
          opacity={0.98}
          width={"bgBoxes.defaultBox"}
          minHeight="100vh"
          maxWidth={"98vw"}
          p={2}
          alignSelf="center"
          color="ui.white"
        >
          <VStack width="100%" align="left">
            <Box width="100%">
              <Text whiteSpace="pre-line">{aboutDescription}</Text>
            </Box>
            <Footer bgColor="ui.main" />
          </VStack>
        </Flex>
      </Flex>
    </Flex>
  );
}
