import {
  AlertDialog,
  AlertDialogBody,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogOverlay,
  Button,
  FormControl,
  FormLabel,
  Input,
  useColorModeValue,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import React from "react";
import { SubmitHandler, useForm } from "react-hook-form";

import { type ApiError, UsersService, UserUpdateMe } from "../../client";
import useCustomToast from "../../hooks/useCustomToast";
import { emailPattern, handleError } from "../../utils";

interface DeleteProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChangeEmailConfirmation = ({ isOpen, onClose }: DeleteProps) => {
  const queryClient = useQueryClient();
  const showToast = useCustomToast();
  const color = useColorModeValue("inherit", "ui.light");
  const cancelRef = React.useRef<HTMLButtonElement | null>(null);
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, errors },
  } = useForm<UserUpdateMe>({
    mode: "onBlur",
    criteriaMode: "all",
  });

  const mutation = useMutation({
    mutationFn: (data: UserUpdateMe) =>
      UsersService.updateMeEmailSendConfirmation({
        requestBody: { email: data.email, username: null },
      }),
    onSuccess: () => {
      showToast(
        "Success",
        "A confirmation email has been sent to the new email to update your email.",
        "success"
      );
      onClose();
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
    },
  });

  const onSubmit: SubmitHandler<UserUpdateMe> = async (data) => {
    data = {
      ...data,
    };
    mutation.mutate(data);
  };

  const handleClose = () => {
    reset(); // Reset the form when closing
    onClose();
  };

  return (
    <>
      <AlertDialog
        isOpen={isOpen}
        onClose={handleClose}
        leastDestructiveRef={cancelRef}
        size={{ base: "sm", md: "md" }}
        isCentered
      >
        <AlertDialogOverlay>
          <AlertDialogContent
            backgroundColor="ui.secondary"
            color="ui.white"
            as="form"
            onSubmit={handleSubmit(onSubmit)}
          >
            <AlertDialogHeader>Change Email</AlertDialogHeader>

            <AlertDialogBody>
              Change email to any available email in this application. A
              confirmation will be sent to the new email.
            </AlertDialogBody>
            <AlertDialogBody>
              <FormControl minWidth={"100%"} isInvalid={!!errors.email}>
                <FormLabel color={color} htmlFor="name">
                  Email
                </FormLabel>
                <Input
                  id="name"
                  {...register("email", {
                    maxLength: {
                      value: 50,
                      message: "Email cannot exceed 50 characters",
                    },
                    pattern: emailPattern,
                    required: "Email is required",
                  })}
                  type="text"
                  size="md"
                  w="auto"
                />
                {errors.email && (
                  <p style={{ color: "red" }}>{errors.email.message}</p>
                )}
              </FormControl>
            </AlertDialogBody>

            <AlertDialogFooter gap={3}>
              <Button
                bg="ui.queryBaseInput"
                _hover={{ bg: "ui.queryMainInput" }}
                variant="danger"
                type="submit"
                isLoading={isSubmitting}
              >
                Update
              </Button>
              <Button
                ref={cancelRef}
                onClick={handleClose}
                isDisabled={isSubmitting}
                bg="ui.lighterSecondary.100"
                color="ui.white"
                _hover={{ bg: "ui.lightInput" }}
              >
                Cancel
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </>
  );
};

export default ChangeEmailConfirmation;
