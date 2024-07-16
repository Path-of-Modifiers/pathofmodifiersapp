import { Box, Flex, Text } from "@chakra-ui/layout";
import AddIconCheckbox from "./AddIconCheckbox";

interface IconTextProps {
  text: string;
  isChecked: boolean;
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  onMouseEnter?: () => void;
}

/** Conains both the AddIconCheckbox and the Text component
 *  with a border */
export const AddICheckText = (props: IconTextProps) => {
  return (
    <Flex alignItems={"center"} gap={2}>
      <AddIconCheckbox {...props}></AddIconCheckbox>
      <Box flex="1" position="relative">
        <Text color="ui.white">{props.text}</Text>
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
    </Flex>
  );
};
