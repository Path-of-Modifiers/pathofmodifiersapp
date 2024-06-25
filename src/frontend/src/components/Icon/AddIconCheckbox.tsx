import { createIcon, Icon } from "@chakra-ui/icons";
import { Box, Checkbox, CheckboxProps } from "@chakra-ui/react";

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
  colorScheme?: string;
}

const AddIcon = (props: AddIconProps) => {
  const { isIndeterminate, isChecked, ...rest } = props;

  return (
    <>
      {isChecked ? (
        <Icon as={WhiteSquareIcon} boxSize="100%" {...rest} />
      ) : isIndeterminate ? (
        <Icon as={WhiteSquareIcon} boxSize="100%" opacity={0.5} {...rest} />
      ) : null}
    </>
  );
};

export const AddIconCheckbox = (props: CheckboxProps) => {
  return (
    <Box
      display="inline-block"
      padding="8px" // Adjust padding to increase clickable area
    >
      <Checkbox
        {...props}
        icon={<AddIcon />}
        isIndeterminate={props.isIndeterminate}
        colorScheme={props.colorScheme || "ui.lightInput"}
        borderColor={props.colorScheme || "ui.lightInput"}
        display="flex"
        alignItems="center"
        justifyContent="center"
        iconSize="1.5em"
      />
    </Box>
  );
};

export default AddIconCheckbox;
