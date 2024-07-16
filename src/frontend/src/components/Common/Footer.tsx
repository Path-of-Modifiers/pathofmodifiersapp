import {
  Stack,
  HStack,
  Link,
  IconButton,
  LinkProps,
  Flex,
  Text,
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
    url: "https://github.com/Ivareh/pathofmodifiersapp",
    label: "Github Repository",
    type: "gray",
    icon: <FaGithub />,
  },
  {
    url: "https://twitter.com/PModifiers85473",
    label: "POM twitter Account",
    type: "twitter",
    icon: <FaTwitter />,
  },
];

const Footer = () => {
  return (
    <Stack
      width="bgBoxes.defaultBox"
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
        spacing={{ base: 8, md: 0 }}
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
            &copy; 2024 company, Inc. All rights reserved.
          </Text>
        </Flex>
      </Stack>
      <Box color="white" mt={7}>
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
