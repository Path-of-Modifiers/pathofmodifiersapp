import {
  Button,
  Container,
  Flex,
  FormControl,
  FormErrorMessage,
  Heading,
  Input,
  Link,
  Text,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import {
  createFileRoute,
  redirect,
  Link as RouterLink,
} from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import { type ApiError, LoginsService } from "../client";
import { isLoggedIn } from "../hooks/validation/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import { emailPattern, handleError } from "../utils";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";

interface FormData {
  email: string;
}

export const Route = createFileRoute("/recover-password")({
  component: RecoverPassword,
  beforeLoad: async () => {
    if (!hasCompletedCaptcha() && !isLoggedIn()) {
      throw redirect({
        to: "/captcha",
        search: () => ({ from: "recover-password" }), // Pass the query parameter using search
      });
    }
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      });
    }
  },
});

function RecoverPassword() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormData>();
  const showToast = useCustomToast();

  const recoverPassword = async (data: FormData) => {
    await LoginsService.recoverPassword({
      requestBody: {
        email: data.email,
      },
    });
  };

  const mutation = useMutation({
    mutationFn: recoverPassword,
    onSuccess: () => {
      showToast(
        "Email sent.",
        "We sent an email with a link to get back into your account.",
        "success"
      );
      reset();
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
  });

  const onSubmit: SubmitHandler<FormData> = async (data) => {
    mutation.mutate(data);
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
          Password Recovery
        </Heading>
        <Text align="center">
          A password recovery email will be sent to the registered account.
        </Text>
        <FormControl isInvalid={!!errors.email}>
          <Input
            id="email"
            {...register("email", {
              required: "Email is required",
              pattern: emailPattern,
            })}
            placeholder="Email"
            type="email"
          />
          {errors.email && (
            <FormErrorMessage>{errors.email.message}</FormErrorMessage>
          )}
        </FormControl>
        <Button
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          variant="primary"
          type="submit"
          isLoading={isSubmitting}
        >
          Continue
        </Button>
        <Text>
          <Link
            as={RouterLink}
            to="/login"
            from="recover-password"
            color="blue.500"
          >
            Back to Log In Page
          </Link>
        </Text>
      </Container>
    </Flex>
  );
}
