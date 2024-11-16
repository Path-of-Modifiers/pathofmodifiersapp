import { Flex, Spinner } from "@chakra-ui/react";
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";

import useTurnstileValidation, {
  hasCompletedCaptcha,
} from "../hooks/validation/turnstileValidation";

import useAuth, { isLoggedIn, isActive } from "../hooks/validation/useAuth";
import { useGraphInputStore } from "../store/GraphInputStore";

const security_ip = localStorage.getItem("security_ip");

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    const searchParams = new URLSearchParams(location.hash.slice(1));
    useGraphInputStore.getState().getStoreFromHash(searchParams);
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
    if (!isActive()) {
      throw redirect({
        to: "/user-not-activated",
      });
    }
  },
});

function Layout() {
  const { isLoadingTurnstile } = useTurnstileValidation({
    token: "",
    ip: security_ip ?? "",
  });

  const { isLoadingUser } = useAuth();

  return (
    <Flex maxW="large" h="auto" position="relative" bgColor="ui.main">
      {isLoadingTurnstile || isLoadingUser ? (
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color={"ui.white"} />
        </Flex>
      ) : (
        <Outlet />
      )}
    </Flex>
  );
}
