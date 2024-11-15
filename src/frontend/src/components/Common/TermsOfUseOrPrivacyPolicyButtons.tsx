import { Flex, Link, Text, FlexProps } from "@chakra-ui/react";
import { Link as RouterLink } from "@tanstack/react-router";

interface TermsOfUseOrPrivacyPolicyButtonsProps extends FlexProps {
  from?: string;
}

const TermsOfUseOrPrivacyPolicyButtons = (
  props: TermsOfUseOrPrivacyPolicyButtonsProps,
) => {
  return (
    <Flex {...props} justifyContent="center">
      <Link
        as={RouterLink}
        to="/terms-of-use"
        from={props.from}
        target="_blank"
        color="blue.500"
      >
        Terms of Use
      </Link>
      <Text mx={3}>|</Text>
      <Link
        as={RouterLink}
        to="/privacy-policy"
        from={props.from}
        target="_blank"
        color="blue.500"
      >
        Privacy Policy
      </Link>
    </Flex>
  );
};

export default TermsOfUseOrPrivacyPolicyButtons;
