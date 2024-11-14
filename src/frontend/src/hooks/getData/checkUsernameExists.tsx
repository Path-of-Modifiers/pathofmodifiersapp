import { useMutation, useQueryClient } from "@tanstack/react-query";
import { type ApiError, UsersService } from "../../client";
import { useState } from "react";

const useCheckUsernameExists = () => {
  const [checkUsernameExistsErrorMessage, setErrorMessage] =
    useState<string>("");
  const [usernameExists, setUsernameExists] = useState<boolean | null>(null);
  const queryClient = useQueryClient();

  const checkUsernameExistsMutation = useMutation({
    mutationFn: (
      username: string, // Accept username as a parameter
    ) => UsersService.checkUsernameExists({ username }),
    onSuccess: (data) => {
      setUsernameExists(data);
    },
    onError: (err: ApiError) => {
      setErrorMessage(err.message);
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
    },
  });

  return {
    usernameExists,
    checkUsernameExistsErrorMessage,
    checkUsernameExistsMutation,
  };
};

export default useCheckUsernameExists;
