import Header from "../../components/Common/Header";
import QueryButtons from "../../components/Common/QueryButtons";
import { GraphInput } from "../../components/Input/GraphInput";
import GraphComponent from "../../components/Graph/GraphComponent";
import Footer from "../../components/Common/Footer";

import { Flex, Box, VStack } from "@chakra-ui/layout";

interface MainPageProps {
  isReady: boolean;
}

export const MainPage = (props: MainPageProps) => {
  return (
    <Flex
      direction="column"
      bg="ui.main"
      width="99vw"
      minWidth="bgBoxes.miniPBox"
    >
      <>
        <Box mb={"7rem"}>
          <Header />
        </Box>

        <Flex
          direction="row"
          bg="ui.secondary"
          justifyContent="center"
          maxWidth={"100%"}
          flexWrap="wrap"
          minHeight="100vh"
          p={3}
          pl={10}
          pr={10}
          borderTopRadius={10}
          borderTopColor={"ui.darkBrown"}
          borderTopWidth={1}
          alignSelf="center"
        >
          {props.isReady && (
            <VStack width={"bgBoxes.defaultBox"} height={"100%"} maxW={"100%"}>
              <GraphInput />
              <QueryButtons />

              <GraphComponent
                width={"bgBoxes.mediumBox"}
                minH={"bgBoxes.smallBox"}
                height={"bgBoxes.smallBox"}
                maxW="98vw"
                mb="10rem"
                justifyItems={"center"}
              />
              <Footer />
            </VStack>
          )}
        </Flex>
      </>
    </Flex>
  );
};
