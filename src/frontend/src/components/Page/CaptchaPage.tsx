import Cookies from "js-cookie";
import { Flex, FlexProps, Text } from "@chakra-ui/layout";
import CaptchaWidget from "../Widget/CaptchaWidget";

export const CaptchaPage = (props: FlexProps) => {
  const status = Cookies.get("cf-captcha-status");
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
      {status === "solved" && (
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          You have successfully completed the captcha. Waiting for website to
          load...
        </Text>
      )}
      {status === "error" && (
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          There was an error with the captcha
        </Text>
      )}
      {status === "expired" && (
        <Text fontSize="xl" textColor="ui.white" mb={"2rem"}>
          The captcha has expired
        </Text>
      )}
      {status === "" && (
        <>
          <Text fontSize="xl" textColor="ui.white" mt={"2rem"}>
            Please complete the captcha to continue to www.pathofmodifiers.com
          </Text>
        </>
      )}
    </Flex>
  );
};

export default CaptchaPage;
