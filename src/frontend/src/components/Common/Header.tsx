import { Flex, Text } from "@chakra-ui/react";

// Header component for the application
const Header = () => {
  return (
    <Flex as="header" align="center" justify="space-between" padding="1rem">
      <Text
        color="ui.white"
        fontSize="30px"
        fontWeight="medium"
      >
        Path of Modifiers
      </Text>
      {/* Add any additional header content here */}
    </Flex>
  );
};

export default Header;
