import { Flex, Spinner } from "@chakra-ui/react";
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";

import useTurnstileValidation, {
  hasCompletedCaptcha,
} from "../hooks/validation/turnstileValidation";

import useAuth, { isLoggedIn } from "../hooks/validation/useAuth";

const security_ip = localStorage.getItem("security_ip");

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    if (!hasCompletedCaptcha()) {
      throw redirect({
        to: "/captcha",
      });
    }
    if (!isLoggedIn()) {
      throw redirect({
        to: "/login",
      });
    }
  },
});

function Layout() {
  const { isLoadingCaptcha } = useTurnstileValidation({
    token: "",
    ip: security_ip ?? "",
  });

  const { isLoadingUser } = useAuth();

  return (
    <Flex maxW="large" h="auto" position="relative" bgColor="ui.main">
      {isLoadingCaptcha || isLoadingUser ? (
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color={"ui.white"} />
        </Flex>
      ) : (
        <Outlet />
      )}
    </Flex>
  );
}
