import { Flex, Spinner } from "@chakra-ui/react";
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";

import useTurnstileValidation, {
  hasCompletedCaptcha,
} from "../hooks/validation/turnstileValidation";

import { useGraphInputStore } from "../store/GraphInputStore";

const security_ip = localStorage.getItem("security_ip");

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    if (!hasCompletedCaptcha()) {
      throw redirect({
        to: "/captcha",
      });
    }
    try {
      const searchParams = new URLSearchParams(location.hash.slice(1));
      useGraphInputStore.getState().getStoreFromHash(searchParams);
    } catch (err) {
      throw redirect({
        to: "/"
      })
    }
  },
});

function Layout() {
  const { isLoadingTurnstile } = useTurnstileValidation({
    token: "",
    ip: security_ip ?? "",
  });

  return (
    <Flex maxW="large" h="auto" position="relative" bgColor="ui.main">
      {isLoadingTurnstile ? (
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color={"ui.white"} />
        </Flex>
      ) : (
        <Outlet />
      )}
    </Flex>
  );
}
