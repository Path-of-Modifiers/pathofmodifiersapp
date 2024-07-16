import { Flex, Text } from "@chakra-ui/react";

// Header component for the application
 const Header = () => {
  return (
    <Flex
      as="header"
      align="center"
      justify="space-between"
      padding="1rem"
    >
      <Text color="ui.white" fontSize="2xl" fontFamily="fonts.heading" fontWeight="fontWeights.bold">
        Path Of Modifiers
      </Text>
      {/* Add any additional header content here */}
    </Flex>
  )
}

export default Header