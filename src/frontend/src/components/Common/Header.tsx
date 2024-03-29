import { Flex, Text } from "@chakra-ui/react";


export default function Header() {
  return (
    <Flex
      as="header"
      align="center"
      justify="space-between"
      padding="1rem"
      boxShadow="md"
      borderBottom="1px solid"
      borderColor="gray.200"
    >
      <Text fontSize="2xl" fontWeight="bold">
        Path Of Modifiers
      </Text>
      {/* Add any additional header content here */}
    </Flex>
  );
}