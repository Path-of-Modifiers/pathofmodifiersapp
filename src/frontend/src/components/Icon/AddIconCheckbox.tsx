import { createIcon, Icon } from "@chakra-ui/icons";
import { Checkbox, CheckboxProps } from "@chakra-ui/react";

// Step 1: Create the White Square Icon
export const WhiteSquareIcon = createIcon({
  displayName: "WhiteSquareIcon",
  viewBox: "0 0 24 24",
  path: <path fill="currentColor" d="M4 4h16v16H4z" />,
});

// Step 2: Create the AddIcon Component
interface AddIconProps {
  isIndeterminate?: boolean;
  isChecked?: boolean;
}

const AddIcon = (props: AddIconProps) => {
  const { isIndeterminate, isChecked, ...rest } = props;

  return (
    <>
      {isChecked ? (
        <Icon as={WhiteSquareIcon} boxSize="100%" {...rest} />
      ) : null}
    </>
  );
};

// Step 3: Create the AddIconCheckbox Component
export const AddIconCheckbox = (props: CheckboxProps) => {
  return (
    <Checkbox
      {...props}
      icon={<AddIcon />}
      colorScheme="ui.lightInput"
      borderColor="ui.lightInput"
      display="flex"
      alignItems="center"
      justifyContent="center"
      iconSize="1.5em"
    />
  );
};

export default AddIconCheckbox;
