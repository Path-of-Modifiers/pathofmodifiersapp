import Cookies from "js-cookie";
import { Flex, FlexProps, Text } from "@chakra-ui/layout";
import CaptchaWidget from "../Widget/CaptchaWidget";
import { useEffect, useState } from "react";

export const CaptchaPage = (props: FlexProps) => {
  const cookieStatus = Cookies.get("cf-captcha-status");
  const [captchaCookieStatus, setCaptchaCookieStatus] = useState<
    string | undefined
  >(cookieStatus);

  useEffect(() => {
    setCaptchaCookieStatus(cookieStatus);
  }, [cookieStatus]);

  return (
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
      {captchaCookieStatus === "solved" && (
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          You have successfully completed the captcha. Waiting for website to
          load...
        </Text>
      )}
      {captchaCookieStatus === "error" && (
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          There was an error with the captcha
        </Text>
      )}
      {captchaCookieStatus === "expired" && (
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          The captcha has expired
        </Text>
      )}
      {!captchaCookieStatus && (
        <Text fontSize="xl" textColor="ui.white" mt={"2rem"}>
          Please complete the captcha to continue to www.pathofmodifiers.com
        </Text>
      )}
    </Flex>
  );
};

export default CaptchaPage;
