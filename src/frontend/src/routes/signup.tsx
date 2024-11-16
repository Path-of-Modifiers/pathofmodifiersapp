import {
  Button,
  Container,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Image,
  Input,
  Link,
  Text,
} from "@chakra-ui/react";
import {
  Link as RouterLink,
  createFileRoute,
  redirect,
} from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import Logo from "/assets/images/POM_logo_rec.svg";
import type { UserRegisterPreEmailConfirmation } from "../client";
import useAuth, { isLoggedIn } from "../hooks/validation/useAuth";
import {
  confirmPasswordRules,
  emailPattern,
  usernamePattern,
  passwordRules,
} from "../utils";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";
import TermsOfUseOrPrivacyPolicyButtons from "../components/Common/TermsOfUseOrPrivacyPolicyButtons";

export const Route = createFileRoute("/signup")({
  component: SignUp,
  beforeLoad: async () => {
    if (!hasCompletedCaptcha() && !isLoggedIn()) {
      throw redirect({
        to: "/captcha",
        search: () => ({ from: "signup" }), // Pass the query parameter using search
      });
    }
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      });
    }
  },
});

interface UserRegisterForm extends UserRegisterPreEmailConfirmation {
  confirm_password: string;
}

function SignUp() {
  const { signUpMutation } = useAuth();
  const {
    register,
    handleSubmit,
    getValues,
    formState: { errors, isSubmitting },
  } = useForm<UserRegisterForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      email: "",
      username: "",
      password: "",
      confirm_password: "",
    },
  });

  const onSubmit: SubmitHandler<UserRegisterForm> = (data) => {
    signUpMutation.mutate(data);
  };

  return (
    <>
      <Flex
        bgColor="ui.main"
        color="ui.white"
        flexDir={{ base: "column", md: "row" }}
        h="loginPages.standardHeight"
        minH="loginPages.standardMinHeight"
      >
        <Container
          as="form"
          onSubmit={handleSubmit(onSubmit)}
          alignItems="stretch"
          mt={"25vh"}
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
          <Text fontSize={"20px"} alignSelf="center">
            Sign up
          </Text>
          <FormControl id="username" isInvalid={!!errors.username}>
            <FormLabel htmlFor="username" srOnly>
              Username
            </FormLabel>
            <Input
              id="username"
              {...register("username", {
                required: "Username is required",
                pattern: usernamePattern,
                maxLength: {
                  value: 30,
                  message: "Username cannot exceed 30 characters",
                },
              })}
              placeholder="Username"
              type="text"
            />
            {errors.username && (
              <FormErrorMessage>{errors.username.message}</FormErrorMessage>
            )}
          </FormControl>
          <FormControl id="email" isInvalid={!!errors.email}>
            <FormLabel htmlFor="username" srOnly>
              Email
            </FormLabel>
            <Input
              id="email"
              {...register("email", {
                required: "Email is required",
                maxLength: 256,
                pattern: emailPattern,
              })}
              placeholder="Email"
              type="email"
            />
            {errors.email && (
              <FormErrorMessage>{errors.email.message}</FormErrorMessage>
            )}
          </FormControl>
          <FormControl id="password" isInvalid={!!errors.password}>
            <FormLabel htmlFor="password" srOnly>
              Password
            </FormLabel>
            <Input
              id="password"
              {...register("password", passwordRules())}
              placeholder="Password"
              type="password"
            />
            {errors.password && (
              <FormErrorMessage>{errors.password.message}</FormErrorMessage>
            )}
          </FormControl>
          <FormControl
            id="confirm_password"
            isInvalid={!!errors.confirm_password}
          >
            <FormLabel htmlFor="confirm_password" srOnly>
              Confirm Password
            </FormLabel>

            <Input
              id="confirm_password"
              {...register("confirm_password", confirmPasswordRules(getValues))}
              placeholder="Repeat Password"
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
            isLoading={isSubmitting}
            isActive={signUpMutation.status === "idle"}
            isDisabled={signUpMutation.status === "pending"}
          >
            Sign Up
          </Button>
          <Text>
            Already have an account?{" "}
            <Link
              as={RouterLink}
              to="/login"
              from="signup"
              key={(Math.random() + 1).toString(36).substring(7)} // Forces reload to make login work
              color="blue.500"
            >
              Log In
            </Link>
          </Text>
          <TermsOfUseOrPrivacyPolicyButtons mt="2rem" from="/signup" />
        </Container>
      </Flex>
    </>
  );
}

export default SignUp;
