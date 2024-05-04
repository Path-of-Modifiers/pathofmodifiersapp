import { Checkbox, CheckboxProps } from "@chakra-ui/react";

import { Icon } from "@chakra-ui/icons";

interface AddIconProps {
  isIndeterminate?: boolean;
  isChecked?: boolean;
}

function AddIcon(props: AddIconProps) {
  const { isIndeterminate, isChecked, ...rest } = props;

  const d = isIndeterminate
    ? "M12,0A12,12,0,1,0,24,12,12.013,12.013,0,0,0,12,0Zm0,19a1.5,1.5,0,1,1,1.5-1.5A1.5,1.5,0,0,1,12,19Zm1.6-6.08a1,1,0,0,0-.6.917,1,1,0,1,1-2,0,3,3,0,0,1,1.8-2.75A2,2,0,1,0,10,9.255a1,1,0,1,1-2,0,4,4,0,1,1,5.6,3.666Z"
    : "M 600.00,133.33 C 636.82,133.33 666.67,163.18 666.67,200.00 666.67,200.00 666.67,600.00 666.67,600.00666.67,636.82 636.82,666.67 600.00,666.67600.00,666.67 200.00,666.67 200.00,666.67 163.18,666.67 133.33,636.82 133.33,600.00 133.33,600.00 133.33,200.00 133.33,200.00 133.33,163.18 163.18,133.33 200.00,133.33 200.00,133.33 600.00,133.33 600.00,133.33 Z";

  return (
    <>
      {isChecked ? (
        <Icon bgColor="ui.white" {...rest}>
          <path fill="currentColor" d={d} />
        </Icon>
      ) : null}
    </>
  );
}

function AddIconCheckbox(props: CheckboxProps) {
  return (
    <Checkbox
      {...props}
      icon={<AddIcon />}
      colorScheme="ui.secondary"
      borderColor={"ui.input"}
    ></Checkbox>
  );
}

export default AddIconCheckbox;
