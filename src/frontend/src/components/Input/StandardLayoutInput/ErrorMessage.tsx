import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
  AlertProps,
} from "@chakra-ui/alert";
import { IconBaseProps } from "react-icons/lib";

interface ErrorMessageProps {
  alertTitle: string;
  alertDescription: string;
  alertIcon?: React.ElementType;
  iconProps?: IconBaseProps;
  alertProps?: AlertProps;
}

export const ErrorMessage = (props: ErrorMessageProps) => {
  let Icon;
  if (props.alertIcon != null) {
    Icon = props.alertIcon;
  } else {
    Icon = AlertIcon;
  }
  return (
    <>
      <Alert {...props.alertProps} status="error">
        <Icon {...props.iconProps} />
        <AlertTitle>{props.alertTitle}</AlertTitle>
        <AlertDescription>{props.alertDescription}</AlertDescription>
      </Alert>
    </>
  );
};
