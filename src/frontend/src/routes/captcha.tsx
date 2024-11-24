import { Center, Container } from "@chakra-ui/layout";
import { createFileRoute, redirect } from "@tanstack/react-router";
import CaptchaPage from "../components/Common/CaptchaPage";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";
import useGetIp from "../hooks/validation/getIp";

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
  useGetIp();

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
