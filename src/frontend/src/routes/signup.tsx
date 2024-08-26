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
import type { UserRegister } from "../client";
import useAuth, { isLoggedIn } from "../hooks/validation/useAuth";
import {
  confirmPasswordRules,
  emailPattern,
  usernamePattern,
  passwordRules,
} from "../utils";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";

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

interface UserRegisterForm extends UserRegister {
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
        h="100vh"
      >
        <Container
          as="form"
          onSubmit={handleSubmit(onSubmit)}
          h="100vh"
          maxW="sm"
          alignItems="stretch"
          mt={"25vh"}
          gap={4}
          centerContent
        >
          <Image
            src={Logo}
            alt="FastAPI logo"
            height="auto"
            maxW="2xs"
            alignSelf="center"
            mb={4}
          />
          <FormControl id="username" isInvalid={!!errors.username}>
            <FormLabel htmlFor="username" srOnly>
              Username
            </FormLabel>
            <Input
              id="username"
              maxLength={50}
              {...register("username", {
                required: "Username is required",
                pattern: usernamePattern,
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
          >
            Sign Up
          </Button>
          <Text>
            Already have an account?{" "}
            <Link as={RouterLink} to="/login" from="signup" color="blue.500">
              Log In
            </Link>
          </Text>
        </Container>
      </Flex>
    </>
  );
}

export default SignUp;
