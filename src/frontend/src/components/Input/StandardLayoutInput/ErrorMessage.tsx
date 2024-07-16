import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
} from "@chakra-ui/alert";

interface ErrorMessageProps {
  alertTitle: string;
  alertDescription: string;
}

export const ErrorMessage = (props: ErrorMessageProps) => {
  return (
    <>
      <Alert status="error">
        <AlertIcon />
        <AlertTitle>{props.alertTitle}</AlertTitle>
        <AlertDescription>{props.alertDescription}</AlertDescription>
      </Alert>
    </>
  );
};
