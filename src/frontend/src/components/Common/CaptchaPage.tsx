import { Flex, FlexProps, Text } from "@chakra-ui/layout";
import { useTurnstileStore } from "../../store/TurnstileStore";
import CaptchaWidget from "../Widget/CaptchaWidget";
import useTurnstileValidation from "../../hooks/validation/turnstileValidation";
import useGetIp from "../../hooks/validation/getIp";
import { Spinner } from "@chakra-ui/react";
import { Outlet } from "@tanstack/react-router";

const security_ip = localStorage.getItem("security_ip");

export const CaptchaPage = (props: FlexProps) => {
  const { turnstileResponse } = useTurnstileStore();
  useGetIp();

  const { isLoading } = useTurnstileValidation({
    token: "",
    ip: security_ip ?? "",
  });

  return (
    <>
      {isLoading ? (
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color="ui.main" />
        </Flex>
      ) : (
        <Outlet />
      )}

      <Flex
        {...props}
        alignItems="center"
        justifyContent="center"
        flexDirection="column"
      >
        <Text fontSize="6xl" textColor="ui.white" mb={"2rem"}>
          www.pathofmodifiers.com
        </Text>
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          Are you human?
        </Text>
        <CaptchaWidget />
        {turnstileResponse?.success && (
          <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
            You have successfully completed the captcha. Waiting for website to
            load...
          </Text>
        )}
        {turnstileResponse?.error_codes && (
          <>
            <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
              There was an error with the captcha.
            </Text>
            <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
              Error: {turnstileResponse.error_codes}
            </Text>
          </>
        )}
        {!turnstileResponse && (
          <Text fontSize="xl" textColor="ui.white" mt={"2rem"}>
            Please complete the captcha to continue to www.pathofmodifiers.com
          </Text>
        )}
      </Flex>
    </>
  );
};

export default CaptchaPage;
