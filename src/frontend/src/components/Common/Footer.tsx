import {
  Stack,
  HStack,
  IconButton,
  Flex,
  Text,
  StackProps,
  Box,
  Link as ChakraLink,
} from "@chakra-ui/react";
import { FaGithub, FaTwitter } from "react-icons/fa";

import CustomLink from "./CustomLink";

const links = [
  { label: "About", url: "/about" },
  { label: "Terms of use", url: "/terms-of-use" },
  { label: "Privacy Policy", url: "/privacy-policy" },
];
const accounts = [
  {
    url: "https://github.com/Path-of-Modifiers/pathofmodifiersapp",
    label: "Github Repository",
    type: "gray",
    icon: <FaGithub />,
  },
  {
    url: "https://x.com/PathOfMods",
    label: "POM twitter Account",
    type: "twitter",
    icon: <FaTwitter />,
  },
];

const Footer = (props: StackProps) => {
  return (
    <Stack
      {...props}
      width="100%"
      mt="auto"
      direction="column"
      color="ui.white"
      justifyContent="space-between"
      marginInline="auto"
      p={15}
    >
      <Stack
        width="100%"
        direction={{ base: "column", md: "row" }}
        justifyContent="space-between"
        mt="auto"
      >
        <Stack
          direction="row"
          spacing={5}
          pt={{ base: 4, md: 0 }}
          alignItems="center"
        >
          {accounts.map((sc, index) => (
            <IconButton
              key={index}
              as={ChakraLink}
              isExternal
              href={sc.url}
              aria-label={sc.label}
              colorScheme={sc.type}
              icon={sc.icon}
              rounded="md"
            />
          ))}
        </Stack>

        {/* Desktop Screen */}
        <HStack spacing={4} alignItems="center">
          {links.map((sc, index) => (
            <CustomLink key={index} internalRoute={sc.url}>
              {sc.label}
            </CustomLink>
          ))}
        </HStack>

        <Flex alignItems="center">
          <Text fontSize="0.875rem" pl="0.5rem">
            &copy; 2024 Path of Modifiers, All rights reserved.
          </Text>
        </Flex>
      </Stack>

      <Box color="white" mt="auto">
        <Text color="ui.grey">
          pathofmodifiers.com is not affiliated with or endorsed by Grinding
          Gear Games.
        </Text>
      </Box>
    </Stack>
  );
};

export default Footer;
