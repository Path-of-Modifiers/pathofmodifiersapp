import { Button, Container, Flex, Heading, Link, Text } from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import {
  createFileRoute,
  redirect,
  Link as RouterLink,
} from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import { type ApiError, UsersService } from "../client";
import useAuth, { isLoggedIn } from "../hooks/validation/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import { handleError } from "../utils";

interface FormData {
  email: string;
}

export const Route = createFileRoute("/user-not-activated")({
  component: UserIsNotActivated,
  beforeLoad: async () => {
    if (!isLoggedIn()) {
      throw redirect({
        to: "/login",
      });
    }
  },
});

function UserIsNotActivated() {
  const {
    handleSubmit,
    reset,
    formState: { isSubmitting },
  } = useForm<FormData>();
  const showToast = useCustomToast();

  const { user, logout } = useAuth();

  const UserIsNotActivated = async () => {
    await UsersService.setActiveUserSendConfirmation();
  };

  const mutation = useMutation({
    mutationFn: UserIsNotActivated,
    onSuccess: () => {
      showToast(
        "Email sent.",
        "We sent an email with a link to get back into your account.",
        "success",
      );
      reset();
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
  });

  const onSubmit: SubmitHandler<FormData> = async () => {
    mutation.mutate();
  };

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
        onSubmit={handleSubmit(onSubmit)}
        maxW="sm"
        alignItems="stretch"
        mt={"25vh"}
        gap={4}
        centerContent
      >
        <Heading size="xl" textAlign="center" mb={2}>
          Hello {user?.username}, your user is not activated.
        </Heading>
        <Text align="center">
          Before you can access Path of Modifiers, you must activate your email.{" "}
          <br /> <br />
          Didn't receive an email? Please click the button below to resend it or
          check your spam folder.
        </Text>
        <Button
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          variant="primary"
          type="submit"
          isLoading={isSubmitting}
          p={7}
        >
          Send activation email to <br /> {user?.email}
        </Button>
        <Text>
          <Link
            as={RouterLink}
            to="/login"
            onClick={logout}
            from="user-not-activated"
            color="blue.500"
          >
            Back to Log In Page (logout)
          </Link>
        </Text>
      </Container>
    </Flex>
  );
}
