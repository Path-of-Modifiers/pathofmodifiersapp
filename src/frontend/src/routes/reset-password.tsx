import {
  Button,
  Container,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Text,
  Image,
} from "@chakra-ui/react";
import { useMutation } from "@tanstack/react-query";
import { createFileRoute, redirect, useNavigate } from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import Logo from "/assets/images/POM_logo_rec.svg";
import { type ApiError, LoginsService, type NewPassword } from "../client";
import { isLoggedIn } from "../hooks/validation/useAuth";
import useCustomToast from "../hooks/useCustomToast";
import { confirmPasswordRules, handleError, passwordRules } from "../utils";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";

interface NewPasswordForm extends NewPassword {
  confirm_password: string;
}

const token = new URLSearchParams(window.location.search).get("token");

export const Route = createFileRoute("/reset-password")({
  component: ResetPassword,
  beforeLoad: async () => {
    if (!token) {
      throw redirect({
        to: "/login",
      });
    }
    if (!hasCompletedCaptcha() && !isLoggedIn()) {
      throw redirect({
        to: "/captcha",
        search: () => ({ from: "reset-password" }), // Pass the query parameter using search
      });
    }
  },
});

function ResetPassword() {
  const {
    register,
    handleSubmit,
    getValues,
    reset,
    formState: { errors },
  } = useForm<NewPasswordForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      new_password: "",
    },
  });
  const showToast = useCustomToast();
  const navigate = useNavigate();

  const resetPassword = async (data: NewPassword) => {
    if (!token) return;
    await LoginsService.resetPassword({
      requestBody: { new_password: data.new_password, token: token },
    });
  };

  const mutation = useMutation({
    mutationFn: resetPassword,
    onSuccess: () => {
      showToast("Success!", "Password updated successfully.", "success");
      reset();
      navigate({ to: "/login" });
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
  });

  const onSubmit: SubmitHandler<NewPasswordForm> = async (data) => {
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
        <Heading size="xl" textAlign="center" mb={2}>
          Reset Password
        </Heading>
        <Text textAlign="center">
          Please enter your new password and confirm it to reset your password.
        </Text>
        <FormControl mt={4} isInvalid={!!errors.new_password}>
          <FormLabel htmlFor="password">Set Password</FormLabel>
          <Input
            id="password"
            {...register("new_password", passwordRules())}
            placeholder="Password"
            type="password"
          />
          {errors.new_password && (
            <FormErrorMessage>{errors.new_password.message}</FormErrorMessage>
          )}
        </FormControl>
        <FormControl mt={4} isInvalid={!!errors.confirm_password}>
          <FormLabel htmlFor="confirm_password">Confirm Password</FormLabel>
          <Input
            id="confirm_password"
            {...register("confirm_password", confirmPasswordRules(getValues))}
            placeholder="Password"
            type="password"
          />
          {errors.confirm_password && (
            <FormErrorMessage>
              {errors.confirm_password.message}
            </FormErrorMessage>
          )}
        </FormControl>
        <Button
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          variant="primary"
          type="submit"
          isActive={mutation.status === "idle"}
          isDisabled={mutation.status === "pending"}
        >
          Reset Password
        </Button>
      </Container>
    </Flex>
  );
}
