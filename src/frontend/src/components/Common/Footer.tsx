import { Flex, FlexProps, Text } from "@chakra-ui/react";

const Footer = (props: FlexProps) => {
  return (
    <Flex
      {...props}
      as="footer"
      py={4}
      padding="1rem"
      textAlign="center"
      color="white"
    >
      <Text>
        pathofmodifiers.com is not affiliated with or endorsed by Grinding Gear
        Games.
      </Text>
    </Flex>
  );
};

export default Footer;
