import { Flex, FlexProps, Text } from "@chakra-ui/layout";
import CaptchaWidget from "../Widget/CaptchaWidget";

export const CaptchaPage = (props: FlexProps) => {
  return (
    <>
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
      </Flex>
    </>
  );
};

export default CaptchaPage;
