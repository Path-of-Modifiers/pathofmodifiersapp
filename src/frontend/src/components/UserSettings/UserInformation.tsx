import {
  Box,
  Button,
  Container,
  Flex,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Heading,
  Input,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { type SubmitHandler, useForm } from "react-hook-form";

import {
  type ApiError,
  type UserPublic,
  type UserUpdateMe,
  UsersService,
} from "../../client";
import useAuth from "../../hooks/validation/useAuth";
import useCustomToast from "../../hooks/useCustomToast";
import { emailPattern, handleError } from "../../utils";

const UserInformation = () => {
  const queryClient = useQueryClient();
  const color = useColorModeValue("inherit", "ui.light");
  const showToast = useCustomToast();
  const [editMode, setEditMode] = useState(false);
  const { user: currentUser } = useAuth();
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { isSubmitting, errors, isDirty },
  } = useForm<UserPublic>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      username: currentUser?.username,
      email: currentUser?.email,
    },
  });

  const toggleEditMode = () => {
    setEditMode(!editMode);
  };

  const mutation = useMutation({
    mutationFn: (data: UserUpdateMe) =>
      UsersService.updateMe({ requestBody: data }),
    onSuccess: () => {
      showToast("Success!", "User updated successfully.", "success");
    },
    onError: (err: ApiError) => {
      handleError(err, showToast);
    },
    onSettled: () => {
      queryClient.invalidateQueries();
    },
  });

  const onSubmit: SubmitHandler<UserUpdateMe> = async (data) => {
    mutation.mutate(data);
  };

  const onCancel = () => {
    reset();
    toggleEditMode();
  };

  return (
    <>
      <Container maxW="full">
        <Heading size="md" py={4}>
          User Information
        </Heading>
        <Box
          w={{ sm: "full", md: "50%" }}
          as="form"
          onSubmit={handleSubmit(onSubmit)}
        >
          <FormControl>
            <FormLabel color={color} htmlFor="name">
              Username
            </FormLabel>
            {editMode ? (
              <Input
                id="name"
                {...register("username", { maxLength: 30 })}
                type="text"
                size="md"
                w="auto"
              />
            ) : (
              <Text
                size="md"
                py={2}
                color={!currentUser?.username ? "ui.dim" : "inherit"}
                isTruncated
                maxWidth="250px"
              >
                {currentUser?.username || "N/A"}
              </Text>
            )}
          </FormControl>
          <FormControl mt={4} isInvalid={!!errors.email}>
            <FormLabel color={color} htmlFor="email">
              Email
            </FormLabel>
            {editMode ? (
              <Input
                id="email"
                {...register("email", {
                  required: "Email is required",
                  pattern: emailPattern,
                })}
                type="email"
                maxWidth="250px"
                size="md"
                w="auto"
              />
            ) : (
              <Text width="inputSizes.lgBox" py={2} isTruncated>
                {currentUser?.email}
              </Text>
            )}
            {errors.email && (
              <FormErrorMessage>{errors.email.message}</FormErrorMessage>
            )}
          </FormControl>
          <Flex mt={4} gap={3}>
            <Button
              variant="primary"
              bgColor="ui.success"
              _hover={{ bgColor: "ui.queryMainInput" }}
              onClick={toggleEditMode}
              type={editMode ? "button" : "submit"}
              isLoading={editMode ? isSubmitting : false}
              isDisabled={editMode ? !isDirty || !getValues("email") : false}
            >
              {editMode ? "Save" : "Edit"}
            </Button>
            {editMode && (
              <Button
                _hover={{ bgColor: "ui.grey" }}
                onClick={onCancel}
                isDisabled={isSubmitting}
              >
                Cancel
              </Button>
            )}
          </Flex>
        </Box>
      </Container>
    </>
  );
};

export default UserInformation;
