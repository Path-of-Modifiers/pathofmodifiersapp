import {
  AlertDialog,
  AlertDialogBody,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogOverlay,
  Button,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import React from "react";
import { useForm } from "react-hook-form";

import { type ApiError, UsersService } from "../../client";
import useAuth from "../../hooks/validation/useAuth";
import useCustomToast from "../../hooks/useCustomToast";
import { handleError } from "../../utils";

interface DeleteProps {
  isOpen: boolean;
  onClose: () => void;
}

const DeleteConfirmation = ({ isOpen, onClose }: DeleteProps) => {
  const queryClient = useQueryClient();
  const showToast = useCustomToast();
  const cancelRef = React.useRef<HTMLButtonElement | null>(null);
  const {
    handleSubmit,
    formState: { isSubmitting },
  } = useForm();
  const { logout } = useAuth();

  const mutation = useMutation({
    mutationFn: () => UsersService.deleteUserMe(),
    onSuccess: () => {
      showToast(
        "Success",
        "Your account has been successfully deleted.",
        "success",
      );
      logout();
      onClose();
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
    },
  });

  const onSubmit = async () => {
    mutation.mutate();
  };

  return (
    <>
      <AlertDialog
        isOpen={isOpen}
        onClose={onClose}
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
            <AlertDialogHeader>Confirmation Required</AlertDialogHeader>

            <AlertDialogBody>
              All your account data will be{" "}
              <strong>permanently deleted.</strong> If you are sure, please
              click <strong>"Confirm"</strong> to proceed. This action cannot be
              undone.
            </AlertDialogBody>

            <AlertDialogFooter gap={3}>
              <Button
                bg="ui.queryBaseInput"
                _hover={{ bg: "ui.queryMainInput" }}
                variant="danger"
                type="submit"
                isLoading={isSubmitting}
                isActive={mutation.status === "idle"}
                isDisabled={mutation.status === "pending"}
              >
                Confirm
              </Button>
              <Button
                ref={cancelRef}
                isDisabled={isSubmitting}
                bg="ui.lighterSecondary.100"
                color="ui.white"
                _hover={{ bg: "ui.lightInput" }}
                onClick={onClose}
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

export default DeleteConfirmation;
