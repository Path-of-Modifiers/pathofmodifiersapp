import { createFileRoute } from "@tanstack/react-router";
import {
  Flex,
  Box,
  VStack,
  Text,
  OrderedList,
  ListItem,
} from "@chakra-ui/layout";

import Header from "../../components/Common/Header";
import Footer from "../../components/Common/Footer";
import { TextWithUnderline } from "../../components/Text/TextWithUnderline";

export const Route = createFileRoute("/_layout/terms-of-use")({
  component: TermsOfUse,
});

// About Route  - This component is the main component for the about route.
function TermsOfUse() {
  return (
    <Flex direction="column" minHeight="100vh" minWidth="98vw" bg="ui.main">
      <Box mb={"7rem"}>
        <Header />
      </Box>

      <Flex
        direction="row"
        bg="ui.secondary"
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
              text="Terms of Use"
              textProps={{ fontSize: "2xl", marginBottom: "1rem" }}
            />
            <Text whiteSpace="pre-line">
              These Terms of Use (the "Terms") govern your use of the Path of
              Modifiers website and services (the "Services") provided by the
              Path of Modifiers Team ("we," "us," or "our"). By accessing or
              using the Services, you agree to be bound by these Terms.
            </Text>
            <OrderedList p="1rem" spacing={2}>
              <ListItem>
                <Text fontWeight="bold">Use of services</Text>
                <Text>
                  1.1 We grant you a personal, non-exclusive, non-transferable,
                  and revocable right to use the Services for private,
                  non-commercial purposes.
                </Text>
                <Text>
                  1.2 You may not use the Services to earn income or for any
                  commercial benefit without explicit permission from us.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Restrictions</Text>
                <Text>
                  2.1 You may not copy, modify, distribute, sell, or lease any
                  part of the Services, nor may you reverse engineer or attempt
                  to extract the source code of the Services, unless laws
                  prohibit those restrictions or you have our written
                  permission.
                </Text>
                <Text>
                  2.2 You may not sublicense or provide the Services to third
                  parties without prior written consent from us.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Ownership</Text>
                <Text>
                  3.1 The Services are provided under a license and are not
                  sold. These Terms do not grant you any rights to our
                  trademarks, trade names, or service marks.
                </Text>
                <Text>
                  3.2 We retain all right, title, and interest in and to the
                  Services, including all intellectual property rights.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Termination</Text>
                <Text>
                  4.1 These Terms are effective until terminated. Your rights
                  under these Terms will terminate automatically without notice
                  from us if you fail to comply with any term(s) of these Terms.
                </Text>
                <Text>
                  4.2 Upon termination of these Terms, you must cease all use of
                  the Services and destroy all copies, full or partial, of any
                  materials obtained from the Services.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Disclaimer of Warranties</Text>
                <Text>
                  5.1 The Services are provided "as is," without warranty of any
                  kind, express or implied, including but not limited to the
                  warranties of merchantability, fitness for a particular
                  purpose, and noninfringement.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Limitation of Liability</Text>
                <Text>
                  6.1 In no event shall we be liable for any special,
                  incidental, indirect, or consequential damages whatsoever
                  (including, without limitation, damages for loss of profits,
                  business interruption, loss of information) arising out of the
                  use of or inability to use the Services, even if we have been
                  advised of the possibility of such damages.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Governing Law</Text>
                <Text>
                  7.1 These Terms shall be governed by and construed in
                  accordance with the laws of Norway, without regard to its
                  conflict of law principles.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight={"bold"}>Contact Information</Text>
                <Text>
                  8.1 If you have a ny questions about these Terms, please
                  contact us at pomodifiers@outlook.com.
                </Text>
              </ListItem>
            </OrderedList>
          </Box>
          <Footer />
        </VStack>
      </Flex>
    </Flex>
  );
}
