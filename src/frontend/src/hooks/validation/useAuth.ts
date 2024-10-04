import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";

import { AxiosError } from "axios";
import {
  type Body_logins_login_access_session as AccessToken,
  type ApiError,
  LoginsService,
  type UserPublic,
  type UserRegisterPreEmailConfirmation,
  UsersService,
} from "../../client";
import useCustomToast from "../useCustomToast";

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null;
};

const useAuth = () => {
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const showToast = useCustomToast();
  const queryClient = useQueryClient();
  const searchParams = new URLSearchParams(window.location.search);
  const from = searchParams.get("from");
  const {
    data: user,
    isLoading: isLoadingUser,
    isError,
  } = useQuery<UserPublic | null, Error>({
    queryKey: ["currentUser", isLoggedIn()],
    queryFn: async () => {
      const user = await UsersService.getUserMe();

      if (!user) {
        localStorage.removeItem("access_token");
        if (from) {
          navigate({ to: "/login" });
        }
      }

      return user; // Add this line to return the user
    },
    retry: false,
    enabled: !!localStorage.getItem("access_token"),
  });

  if (isError) {
    localStorage.removeItem("access_token");
    navigate({ to: from ? "/" + `${from}` : "/login" });
  }

  const signUpMutation = useMutation({
    mutationFn: (data: UserRegisterPreEmailConfirmation) =>
      UsersService.registerUserSendConfirmation({ requestBody: data }),

    onSuccess: () => {
      navigate({ to: "/login" });
      showToast(
        "Account created.",
        "Your account has been created successfully.",
        "success"
      );
    },
    onError: (err: ApiError) => {
      let errDetail = err.body?.detail;

      if (err instanceof AxiosError) {
        errDetail = err.message;
      }

      showToast("Something went wrong.", errDetail, "error");
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["users"] });
    },
  });

  const login = async (data: AccessToken) => {
    const response = await LoginsService.loginAccessSession({
      formData: data,
    });
    localStorage.setItem("access_token", response.access_token);
  };

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      localStorage.removeItem("turnstile_captcha_token");
      navigate({ to: "/" });
    },
    onError: (err: ApiError) => {
      let errDetail = err.body?.detail;

      if (err instanceof AxiosError) {
        errDetail = err.message;
      }

      if (Array.isArray(errDetail)) {
        errDetail = "Something went wrong";
      }

      setError(errDetail);
    },
  });

  const logout = () => {
    localStorage.removeItem("access_token");
    navigate({ to: "/login" });
  };

  return {
    signUpMutation,
    loginMutation,
    logout,
    user,
    isLoadingUser,
    error,
    resetError: () => setError(null),
  };
};

export { isLoggedIn };
export default useAuth;
