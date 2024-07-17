import { Flex, Link, Text } from "@chakra-ui/react";

// Header component for the application
const Header = () => {
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
      {/* Add any additional header content here */}
    </Flex>
  );
};

export default Header;
