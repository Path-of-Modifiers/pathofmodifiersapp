import { createFileRoute, Link as RouterLink } from "@tanstack/react-router";

import {
  Flex,
  Box,
  VStack,
  Text,
  Link,
  OrderedList,
  ListItem,
} from "@chakra-ui/react";

import Footer from "../components/Common/Footer";

export const Route = createFileRoute("/terms-of-use")({
  component: TermsOfUse,
});

// About Route  - This component is the main component for the about route.
function TermsOfUse() {
  return (
    <Flex
      direction="column"
      bg="ui.main"
      width="99vw"
      minWidth="bgBoxes.miniPBox"
      alignItems="center"
    >
      <Box width="full" padding="1rem">
        <Link
          color="ui.white"
          fontSize="30px"
          fontWeight="medium"
          as={RouterLink}
          to="/"
          from="terms-of-use"
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
        minHeight="100vh"
        height="100rem"
        width={"bgBoxes.defaultBox"}
        maxWidth={"98vw"}
        p={2}
        color="ui.white"
      >
        <VStack width="100%" align="left">
          <Box width="100%">
            <VStack alignItems="center" mb="2rem">
              <Text justifySelf="center" fontSize={50}>
                Terms of Use
              </Text>
              <Text fontWeight={"bold"}>Effective date: 15.11.2024</Text>
            </VStack>
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
                  contact us at team@pathofmodifiers.com.
                </Text>
              </ListItem>
            </OrderedList>
          </Box>
        </VStack>
        <Footer bgColor="ui.main" />
      </Flex>
    </Flex>
  );
}
