import {
  Container,
  Flex,
  Heading,
  Box,
  Tab,
  TabList,
  VStack,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";

import ChangePassword from "../../components/UserSettings/ChangePassword";
import DeleteAccount from "../../components/UserSettings/DeleteAccount";
import UserInformation from "../../components/UserSettings/UserInformation";
import Header from "../../components/Common/Header";
import Footer from "../../components/Common/Footer";

const tabsConfig = [
  { title: "Profile", component: UserInformation },
  { title: "Password", component: ChangePassword },
  { title: "Danger zone", component: DeleteAccount },
];

export const Route = createFileRoute("/_layout/settings")({
  component: UserSettings,
});

function UserSettings() {
  // Future reference if Superuser wants more tabs
  // const queryClient = useQueryClient();
  // const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"]);
  // const finalTabs = currentUser?.isSuperuser
  //   ? tabsConfig
  //   : tabsConfig.slice(0, 3);

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
          justifyContent="center"
          maxWidth={"100%"}
          flexWrap="wrap"
          minHeight="100vh"
          p={3}
          pl={10}
          pr={10}
          alignSelf="center"
        >
          <VStack width={"bgBoxes.defaultBox"} height={"100%"} maxW={"100%"}>
            <Container color="ui.white" centerContent h="100vh">
              <Heading
                size="lg"
                textAlign={{ base: "center", md: "left" }}
                py={12}
              >
                User Settings
              </Heading>
              <Tabs
                variant="enclosed"
                width="bgBoxes.tinyBox"
                maxWidth="100vw"
                bgColor="ui.secondary"
                borderRadius={10}
                borderTopColor={"ui.darkBrown"}
                borderTopWidth={1}
                borderBottomRadius={10}
              >
                <TabList borderColor="ui.lighterSecondary.100">
                  {tabsConfig.map((tab, index) => (
                    <Tab
                      key={index}
                      _selected={{
                        color: "ui.inputChanged",
                        textDecoration: "underline",
                        fontWeight: "bold",
                      }}
                      _hover={{
                        color: "ui.inputChanged",
                      }}
                    >
                      {tab.title}
                    </Tab>
                  ))}
                </TabList>
                <TabPanels>
                  {tabsConfig.map((tab, index) => (
                    <TabPanel key={index}>
                      <tab.component />
                    </TabPanel>
                  ))}
                </TabPanels>
              </Tabs>
            </Container>
            <Footer />
          </VStack>
        </Flex>
      </>
    </Flex>
  );
}
