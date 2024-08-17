import { Flex, Spinner } from "@chakra-ui/react";
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";

import useTurnstileValidation, {
  hasCompletedCaptcha,
} from "../schemas/validation/turnstileValidation";

const security_ip = localStorage.getItem("security_ip");

export const Route = createFileRoute("/_layout")({
  component: Layout,
  beforeLoad: async () => {
    if (!hasCompletedCaptcha()) {
      throw redirect({
        to: "/captcha",
      });
    }
  },
});

function Layout() {
  const { isLoading } = useTurnstileValidation({
    token: "",
    ip: security_ip ?? "",
  });

  return (
    <Flex maxW="large" h="auto" position="relative" bgColor="ui.main">
      {isLoading ? (
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color={"ui.white"} />
        </Flex>
      ) : (
        <Outlet />
      )}
    </Flex>
  );
}
