import {
  Stack,
  HStack,
  Link,
  IconButton,
  LinkProps,
  Flex,
  Text,
  StackProps,
  Box,
} from "@chakra-ui/react";
// Here we have used react-icons package for the icons
import { FaGithub, FaTwitter } from "react-icons/fa";

const links = [
  { label: "About", url: "about" },
  { label: "Terms of use", url: "terms-of-use" },
  { label: "Privacy Policy", url: "privacy-policy" },
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
      minHeight="10rem"
      mt="auto"
      direction="column"
      bg="ui.secondary"
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
              as={Link}
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
            <CustomLink key={index} hrefRoute={sc.url}>
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

interface CustomLinkProps extends LinkProps {
  hrefRoute: string;
}

const CustomLink = ({ children, hrefRoute, ...props }: CustomLinkProps) => {
  return (
    <Link
      href={hrefRoute}
      fontSize="sm"
      _hover={{ textDecoration: "underline" }}
      {...props}
    >
      {children}
    </Link>
  );
};

export default Footer;
