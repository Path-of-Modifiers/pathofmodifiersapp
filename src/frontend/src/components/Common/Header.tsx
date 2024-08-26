import { Flex, Link, Text } from "@chakra-ui/react";
import useAuth from "../../hooks/validation/useAuth";

// Header component for the application
const Header = () => {
  const { user: currentUser } = useAuth();
  return (
    <Flex as="header" align="center" justify="space-between" padding="1rem">
      <Link href={"/"}>
        <Text
          color="ui.white"
          fontSize="30px"
          fontWeight="medium"
          _hover={{ color: "ui.inputChanged", textDecoration: "underline" }}
        >
          Path of Modifiers
        </Text>
      </Link>
      <Link href={"/settings"}>
        <Text
          color="ui.white"
          fontSize="20px"
          fontWeight="medium"
          _hover={{ color: "ui.inputChanged", textDecoration: "underline" }}
        >
          {currentUser?.username}
        </Text>
      </Link>
    </Flex>
  );
};

export default Header;
