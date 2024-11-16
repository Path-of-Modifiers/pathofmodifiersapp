import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  Flex,
  FormControl,
  FormErrorMessage,
  Icon,
  Image,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Text,
  useBoolean,
} from "@chakra-ui/react";
import {
  Link as RouterLink,
  createFileRoute,
  redirect,
} from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import Logo from "/assets/images/POM_logo_rec.svg";
import type { Body_logins_login_access_session as AccessToken } from "../client";
import useAuth, { isLoggedIn } from "../hooks/validation/useAuth";
import useTurnstileValidation, {
  hasCompletedCaptcha,
} from "../hooks/validation/turnstileValidation";
import TermsOfUseOrPrivacyPolicyButtons from "../components/Common/TermsOfUseOrPrivacyPolicyButtons";

export const Route = createFileRoute("/login")({
  component: Login,
  beforeLoad: async () => {
    if (!hasCompletedCaptcha() && !isLoggedIn()) {
      throw redirect({
        to: "/captcha",
        search: () => ({ from: "login" }), // Pass the query parameter using search
      });
    } else if (isLoggedIn()) {
      throw redirect({
        to: "/",
      });
    }
  },
});

function Login() {
  useTurnstileValidation();
  const [show, setShow] = useBoolean();
  const { loginMutation, checkIsActiveMutation, error, resetError } = useAuth();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<AccessToken>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    if (isSubmitting) return;

    resetError();

    try {
      await loginMutation.mutateAsync(data);
      await checkIsActiveMutation();
    } catch {
      // error is handled by useAuth hook
    }
  };

  return (
    <Flex
      bgColor="ui.main"
      color="ui.white"
      h="loginPages.standardHeight"
      minH="loginPages.standardMinHeight"
    >
      <Container
        as="form"
        onSubmit={handleSubmit(onSubmit)}
        maxW="sm"
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
          Login
        </Text>
        <FormControl
          id="emailOrUsername"
          isInvalid={!!errors.username || !!error}
        >
          <Input
            id="emailOrUsername"
            {...register("username", {
              required: "Email or Username is required",
            })}
            placeholder="Email or Username"
            required
          />
          {errors.username && (
            <FormErrorMessage>{errors.username.message}</FormErrorMessage>
          )}
        </FormControl>
        <FormControl id="password" isInvalid={!!error}>
          <InputGroup>
            <Input
              {...register("password", {
                required: "Password is required",
              })}
              type={show ? "text" : "password"}
              placeholder="Password"
              required
            />
            <InputRightElement
              _hover={{
                cursor: "pointer",
              }}
            >
              <Icon
                as={show ? ViewOffIcon : ViewIcon}
                onClick={setShow.toggle}
                aria-label={show ? "Hide password" : "Show password"}
              >
                {show ? <ViewOffIcon /> : <ViewIcon />}
              </Icon>
            </InputRightElement>
          </InputGroup>
          {error && <FormErrorMessage>{error}</FormErrorMessage>}
        </FormControl>
        <Text>
          <Link
            as={RouterLink}
            to="/recover-password"
            from="login"
            color="blue.500"
          >
            Forgot password?
          </Link>
        </Text>
        <Button
          bg="ui.queryBaseInput"
          color="ui.white"
          _hover={{ bg: "ui.queryMainInput" }}
          variant="primary"
          type="submit"
          isLoading={isSubmitting}
        >
          Log In
        </Button>
        <Text>
          Don't have an account?{" "}
          <Link as={RouterLink} to="/signup" from="login" color="blue.500">
            Sign up
          </Link>
        </Text>
        <TermsOfUseOrPrivacyPolicyButtons mt="2rem" from="/login" />
      </Container>
    </Flex>
  );
}
