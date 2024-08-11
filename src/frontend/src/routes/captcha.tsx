import { Center, Flex } from "@chakra-ui/layout";
import { createFileRoute, redirect } from "@tanstack/react-router";
import { useEffect, useRef } from "react";
import CaptchaPage from "../components/Common/CaptchaPage";
import { hasCompletedCaptcha } from "../hooks/validation/turnstileValidation";

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

  useEffect(() => {
    if (!isFetched.current) {
      console.log("");

      isFetched.current = true; // Mark as fetched
    }
  }, []);
  return (
    <>
      <Flex
        direction="column"
        minHeight="100rem"
        bg="ui.main"
        width="99vw"
        minWidth="bgBoxes.miniPBox"
      >
        <Center mt={"7rem"}>
          <CaptchaPage />
        </Center>
      </Flex>
    </>
  );
}
