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
import { handleError, usernamePattern } from "../../utils";

interface DeleteProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChangeUsernameConfirmation = ({ isOpen, onClose }: DeleteProps) => {
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
      UsersService.updateMeUsername({
        requestBody: { username: data.username },
      }),
    onSuccess: () => {
      showToast(
        "Success",
        "Successfully updated to the new username.",
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
            <AlertDialogHeader>Change Username</AlertDialogHeader>

            <AlertDialogBody>
              Change username to any available username in this application. The
              update takes effect immediately. <br /> <br />
              Can only be done once a month.
            </AlertDialogBody>
            <AlertDialogBody>
              <FormControl minWidth={"100%"} isInvalid={!!errors.username}>
                <FormLabel color={color} htmlFor="name">
                  Username
                </FormLabel>
                <Input
                  id="name"
                  {...register("username", {
                    maxLength: {
                      value: 50,
                      message: "Username cannot exceed 50 characters",
                    },
                    pattern: usernamePattern,
                    required: "Username is required",
                  })}
                  type="text"
                  size="md"
                  w="auto"
                />
                {errors.username && (
                  <p style={{ color: "red" }}>{errors.username.message}</p>
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

export default ChangeUsernameConfirmation;
