import { Flex, Text } from "@chakra-ui/react";


 const Header = () => {
  return (
    <Flex
      as="header"
      align="center"
      justify="space-between"
      padding="1rem"
      boxShadow="md"
      bg="ui.main"
      borderColor="gray.200"
    >
      <Text color="ui.white" fontSize="2xl" fontFamily="fonts.heading" fontWeight="fontWeights.bold">
        Path Of Modifiers
      </Text>
      {/* Add any additional header content here */}
    </Flex>
  )
}

export default Header