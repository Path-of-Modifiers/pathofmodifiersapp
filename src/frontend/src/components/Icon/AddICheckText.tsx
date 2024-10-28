import { Flex } from "@chakra-ui/layout";
import { AddIconCheckbox } from "./AddIconCheckbox";
import { TextWithUnderline } from "../Text/TextWithUnderline";

interface IconTextProps {
  text: string;
  isChecked: boolean;
  onChange: React.ChangeEventHandler<HTMLInputElement>;
  onMouseEnter?: () => void;
}

/** Contains both the AddIconCheckbox and the Text component
 *  with a border */
export const AddICheckText = (props: IconTextProps) => {
  return (
    <Flex alignItems={"center"} gap={2}>
      <AddIconCheckbox {...props}></AddIconCheckbox>
      <TextWithUnderline text={props.text} textProps={{ color: "ui.white" }} />
    </Flex>
  );
};
