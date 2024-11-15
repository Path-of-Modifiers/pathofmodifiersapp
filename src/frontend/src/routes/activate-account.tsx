import {
  Container,
  Flex,
  Heading,
  Image,
  VStack,
  Text,
  Link,
} from "@chakra-ui/react";
import {
  createFileRoute,
  redirect,
  Link as RouterLink,
} from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";

import Logo from "/assets/images/POM_logo_rec.svg";
import { UsersService, ApiError } from "../client";
import { isLoggedIn } from "../hooks/validation/useAuth";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";

const token = new URLSearchParams(window.location.search).get("token");
export const Route = createFileRoute("/activate-account")({
  component: ActivateAccount,
  beforeLoad: async () => {
    if (!token) {
      throw redirect({
        to: "/login",
      });
    }
    if (!hasCompletedCaptcha() && !isLoggedIn()) {
      throw redirect({
        to: "/captcha",
        search: () => ({ from: "activate-account" }), // Pass the query parameter using search
      });
    }
  },
});

function ActivateAccount() {
  const {
    data: response,
    isLoading,
    isSuccess,
    isError,
    error,
  } = useQuery({
    queryKey: ["userConfirm"],
    queryFn: async () => {
      if (!token) return;
      const response = await UsersService.registerUserConfirm({
        requestBody: { access_token: token },
      });
      return response;
    },
    retry: (failureCount, error) =>
      failureCount < 3 &&
      error instanceof ApiError &&
      error.status !== 401 &&
      error.status !== 429,
    retryDelay: 1500,
  });

  return (
    <Flex
      bgColor="ui.main"
      color="ui.white"
      h="loginPages.standardHeight"
      minH="loginPages.standardMinHeight"
    >
      <Container
        bgColor="ui.main"
        color="ui.white"
        as="form"
        maxW="sm"
        alignItems="stretch"
        mt={"15vh"}
        gap={4}
        centerContent
      >
        <Image
          src={Logo}
          alt="POM logo"
          height="auto"
          maxW="2xs"
          alignSelf="center"
          mb={4}
        />

        {isLoading ? (
          <Heading size="lg" textAlign="center" mb={2}>
            Checking user activation token...
          </Heading>
        ) : isSuccess ? (
          <VStack>
            <Heading size="xl" textAlign="center" mb={2}>
              Successfully activated the user!
            </Heading>
            <Text>{response?.message ?? "Unknown"}</Text>
          </VStack>
        ) : isError ? (
          <VStack>
            <Heading size="lg" textAlign="center" mb={2}>
              Failed to activate the user.
            </Heading>
            <Text>Error: {error.message ?? "Unknown"}</Text>
          </VStack>
        ) : (
          <Heading size="lg" textAlign="center" mb={2}>
            Activating user...
          </Heading>
        )}
        {isLoggedIn() ? (
          <Link as={RouterLink} to="/" from="activate-account" color="blue.500">
            Back to Home Page
          </Link>
        ) : (
          <Link
            as={RouterLink}
            to="/login"
            from="activate-account"
            key={(Math.random() + 1).toString(36).substring(7)} // Forces reload to make login work
            color="blue.500"
          >
            Back to Log In Page
          </Link>
        )}
      </Container>
    </Flex>
  );
}
