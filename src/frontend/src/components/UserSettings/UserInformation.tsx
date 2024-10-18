import {
  VStack,
  Button,
  Container,
  Heading,
  HStack,
  Text,
  useDisclosure,
} from "@chakra-ui/react";

import EditInputIcon from "../Icon/EditInputIcon";
import useAuth from "../../hooks/validation/useAuth";
import ChangeUsernameConfirmation from "./ChangeUsernameConfirmation";
import ChangeEmailConfirmation from "./ChangeEmailConfirmation";

const UserInformation = () => {
  const { user: currentUser } = useAuth();
  const confirmationUsernameModal = useDisclosure();
  const confirmationEmailModal = useDisclosure();

  return (
    <>
      <Container maxW="full">
        <Heading size="md" py={4}>
          User Information
        </Heading>
        <VStack gap={4} w={{ sm: "full", md: "full" }} as="form">
          <HStack width="full">
            <Text size="md" py={2} isTruncated maxWidth="250px" mr="auto">
              Username
            </Text>
            <HStack
              width="inputSizes.mdPlusBox"
              bgColor="ui.lighterSecondary.100"
              borderRadius={4}
            >
              <Text
                width="full"
                borderRadius={4}
                borderRightRadius={0}
                borderWidth={1}
                borderColor={"ui.greyShade.100"}
                color="ui.greyShade.200"
                p="6px"
                mr={-2}
              >
                {currentUser?.username || "N/A"}
              </Text>

              <Button
                leftIcon={<EditInputIcon boxSize={4} color="white" ml="6px" />}
                variant="primary"
                onClick={confirmationUsernameModal.onOpen}
                width="40px"
                _hover={{
                  bg: "ui.lighterSecondary.200",
                }}
              />
            </HStack>

            <ChangeUsernameConfirmation
              isOpen={confirmationUsernameModal.isOpen}
              onClose={confirmationUsernameModal.onClose}
            />
          </HStack>

          <HStack width="full">
            <Text size="md" py={2} isTruncated maxWidth="250px" mr="auto">
              Email
            </Text>
            <HStack
              width="inputSizes.mdPlusBox"
              bgColor="ui.lighterSecondary.100"
              borderRadius={4}
            >
              <Text
                width="full"
                borderRadius={4}
                borderRightRadius={0}
                borderWidth={1}
                borderColor={"ui.greyShade.100"}
                color="ui.greyShade.200"
                p="6px"
                mr={-2}
              >
                {currentUser?.email || "N/A"}
              </Text>

              <Button
                leftIcon={<EditInputIcon boxSize={4} color="white" ml="6px" />}
                variant="primary"
                onClick={confirmationEmailModal.onOpen}
                width="40px"
                _hover={{
                  bg: "ui.lighterSecondary.200",
                }}
              />
            </HStack>

            <ChangeEmailConfirmation
              isOpen={confirmationEmailModal.isOpen}
              onClose={confirmationEmailModal.onClose}
            />
          </HStack>
        </VStack>
      </Container>
    </>
  );
};

export default UserInformation;
