import { Center, Container } from "@chakra-ui/layout";
import { createFileRoute, redirect } from "@tanstack/react-router";
import { useEffect, useRef } from "react";
import CaptchaPage from "../components/Common/CaptchaPage";
import useTurnstileValidation, {
  hasCompletedCaptcha,
} from "../hooks/validation/turnstileValidation";
import useGetIp from "../hooks/validation/getIp";

const security_ip = localStorage.getItem("security_ip");

export const Route = createFileRoute("/captcha")({
  component: Captcha,
  beforeLoad: async () => {
    if (hasCompletedCaptcha()) {
      throw redirect({
        to: "/",
      });
    }
  },
});

// Index Component  -  This component is the main component for the index route.
function Captcha() {
  const isFetched = useRef(false);
  useGetIp();
  useTurnstileValidation({
    token: "",
    ip: security_ip ?? "",
  });

  useEffect(() => {
    if (!isFetched.current) {
      console.log("");

      isFetched.current = true; // Mark as fetched
    }
  }, []);

  return (
    <Container
      minHeight="100rem"
      bg="ui.main"
      maxW="100wh"
      p={100}
      h="100vh"
      minWidth="bgBoxes.miniPBox"
    >
      <Center>
        <CaptchaPage />
      </Center>
    </Container>
  );
}
