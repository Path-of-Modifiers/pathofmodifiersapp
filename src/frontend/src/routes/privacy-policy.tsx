import { createFileRoute, Link as RouterLink } from "@tanstack/react-router";

import {
  Flex,
  Box,
  UnorderedList,
  VStack,
  Text,
  Link,
  OrderedList,
  ListItem,
} from "@chakra-ui/react";

import Footer from "../components/Common/Footer";

export const Route = createFileRoute("/privacy-policy")({
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
          from="privacy-policy"
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
        minHeight="140vh"
        width={"bgBoxes.defaultBox"}
        maxWidth={"98vw"}
        p={2}
        color="ui.white"
      >
        <VStack alignItems="center">
          <Text justifySelf="center" fontSize={50}>
            Privacy Policy
          </Text>
          <Text fontWeight={"bold"}>Effective date: 01.03.2025</Text>
        </VStack>
        <VStack width="100%" align="left">
          <Box width="100%" mb="3rem">
            <Text whiteSpace="pre-line">
              This Privacy Policy explains how Path of Modifiers ("we," "us," or
              "our") collects, uses, stores, and protects your information when
              you visit our website and use our services. By using our website,
              you agree to the collection and use of information in accordance
              with this policy.
            </Text>
            <OrderedList p="1rem" spacing={2}>
              <ListItem>
                <Text fontWeight="bold">Information We Collect</Text>
                <Text fontWeight="bold">1.1 Personal Data:</Text>
                <UnorderedList>
                  <ListItem>
                    <b>Contact Information:</b> Email addresses when you contact
                    us for support or inquiries.
                  </ListItem>
                </UnorderedList>
                <Text fontWeight="bold">1.2 Usage Data:</Text>
                <UnorderedList>
                  <ListItem>
                    <b>Log Data:</b> IP address, browser type, browser version,
                    the pages of our website that you visit, the time and date
                    of your visit, the time spent on those pages, and other
                    diagnostic data.
                  </ListItem>
                  <ListItem>
                    <b>Cookies and Tracking Technologies:</b> We use cookies and
                    similar tracking technologies to track activity on our
                    website and hold certain information.
                  </ListItem>
                </UnorderedList>
                <Text fontWeight="bold">1.3 Ad Data:</Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">How We Store Your Data</Text>
                <Text>
                  We store your data securely using industry-standard encryption
                  and security measures. Data is stored on servers located in
                  Sweden. We take appropriate measures to ensure your data is
                  protected against unauthorized access, alteration, or
                  destruction.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">How We Use Your Data</Text>
                <Text>
                  <b>3.1 Current Uses:</b>
                </Text>
                <UnorderedList>
                  <ListItem>
                    To provide and maintain our website and services.
                  </ListItem>
                  <ListItem>
                    To notify you about changes to our services.
                  </ListItem>
                  <ListItem>
                    To allow you to participate in interactive features of our
                    website.
                  </ListItem>
                  <ListItem>To provide customer support.</ListItem>
                  <ListItem>
                    To gather analysis or valuable information so that we can
                    improve our website.
                  </ListItem>
                  <ListItem>To monitor the usage of our website.</ListItem>
                  <ListItem>
                    To detect, prevent, and address technical issues.
                  </ListItem>
                </UnorderedList>
                <Text>
                  <b>3.2 Future Uses:</b>
                </Text>
                <UnorderedList>
                  <ListItem>
                    We may use your data to show personalized advertisements based on your usage
                    data.
                  </ListItem>
                  <ListItem>
                    We may use your data to develop new services or enhance
                    existing ones.
                  </ListItem>
                  <ListItem>
                    We may use your data for additional marketing purposes,
                    subject to updating this policy accordingly.
                  </ListItem>
                </UnorderedList>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Purpose of Data Collection</Text>
                <Text>We collect, store, and use your data to:</Text>
                <UnorderedList>
                  <ListItem>Improve user experience.</ListItem>
                  <ListItem>Personalize and improve our services.</ListItem>
                  <ListItem>
                    Generate revenue through targeted advertisements.
                  </ListItem>
                  <ListItem>
                    Ensure the security and stability of our website.
                  </ListItem>
                </UnorderedList>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Data Retention</Text>
                <Text>
                  We retain your personal data only for as long as necessary for
                  the purposes set out in this Privacy Policy. Usage data is
                  generally retained for a shorter period, except when this data
                  is used to strengthen the security or to improve the
                  functionality of our website, or we are legally obligated to
                  retain this data for longer time periods.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Opt-Out Policy</Text>
                <Text>
                  Under The Consumer Authority (CA) and other applicable laws,
                  you have the right to opt out of the sale of your personal
                  information and to request the deletion of your data. To opt
                  out or request deletion, please contact us at
                  team@pathofmodifiers.com. We will respond to your request
                  within the time frame required by law.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Changes to This Privacy Policy</Text>
                <Text>
                  We may update our Privacy Policy from time to time. We will
                  notify you of any changes by posting the new Privacy Policy on
                  this page. You are advised to review this Privacy Policy
                  periodically for any changes.
                </Text>
              </ListItem>
              <ListItem>
                <Text fontWeight="bold">Contact Us</Text>
                <Text>
                  If you have any questions about this Privacy Policy, please
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
