import {
  Container,
  Flex,
  Heading,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";
import { useQueryClient } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";

import type { UserPublic } from "../../client";
import ChangePassword from "../../components/UserSettings/ChangePassword";
import DeleteAccount from "../../components/UserSettings/DeleteAccount";
import UserInformation from "../../components/UserSettings/UserInformation";
import Header from "../../components/Common/Header";

const tabsConfig = [
  { title: "My profile", component: UserInformation },
  { title: "Password", component: ChangePassword },
  { title: "Danger zone", component: DeleteAccount },
];

export const Route = createFileRoute("/_layout/settings")({
  component: UserSettings,
});

function UserSettings() {
  const queryClient = useQueryClient();
  const currentUser = queryClient.getQueryData<UserPublic>(["currentUser"]);
  const finalTabs = currentUser?.isSuperuser
    ? tabsConfig.slice(0, 3)
    : tabsConfig;

  return (
    <Flex
      direction="column"
      bg="ui.main"
      width="99vw"
      minHeight="200vh"
      height="100vh"
      minWidth="bgBoxes.miniPBox"
    >
      <Header />
      <Container maxW="full" color="ui.white" centerContent h="100vh">
        <Heading size="lg" textAlign={{ base: "center", md: "left" }} py={12}>
          User Settings
        </Heading>
        <Tabs
          variant="enclosed"
          width="bgBoxes.tinyBox"
          bgColor="ui.secondary"
          borderTopRadius={10}
          borderTopColor={"ui.darkBrown"}
          borderTopWidth={1}
        >
          <TabList>
            {finalTabs.map((tab, index) => (
              <Tab key={index}>{tab.title}</Tab>
            ))}
          </TabList>
          <TabPanels>
            {finalTabs.map((tab, index) => (
              <TabPanel key={index}>
                <tab.component />
              </TabPanel>
            ))}
          </TabPanels>
        </Tabs>
      </Container>
    </Flex>
  );
}
