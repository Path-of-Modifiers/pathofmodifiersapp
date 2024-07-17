import { Box, Text, TextProps } from "@chakra-ui/layout";

interface TextWithUnderlineProps {
  text: string;
  textProps?: TextProps;
}
/** Conains both the AddIconCheckbox and the Text component
 *  with a border */
export const TextWithUnderline = (props: TextWithUnderlineProps) => {
  return (
    <Box flex="1" position="relative">
      <Text color="ui.white" {...props.textProps}>
        {props.text}
      </Text>
      <Box
        position="absolute"
        top="2"
        bottom="0"
        left="0"
        right="0"
        borderBottom="1px solid"
        borderColor="ui.grey"
      />
    </Box>
  );
};
