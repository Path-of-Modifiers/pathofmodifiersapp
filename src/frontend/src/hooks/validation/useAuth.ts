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

export const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null;
};

export const isActive = () => {
  return localStorage.getItem("is_active") !== null;
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
    queryKey: ["currentUser"],
    queryFn: async () => {
      const user = await UsersService.getUserMe();

      if (!user) {
        localStorage.removeItem("access_token");
        if (from) {
          navigate({ to: "/login" });
        }
      }
      if (!user.isActive) {
        localStorage.setItem("is_active", "true");
        navigate({ to: "/user-not-activated" });
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
        "Your account has been created successfully. Please check your email for confirmation.",
        "success",
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
      queryClient.invalidateQueries({ queryKey: ["currentUser"] });
    },
  });

  const login = async (data: AccessToken) => {
    const response = await LoginsService.loginAccessSession({
      formData: data,
    });
    queryClient.clear();
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

  const checkIsActiveMutation = async () => {
    const response = await UsersService.checkCurrentUserActive();
    if (!response) {
      localStorage.setItem("is_active", "");
      navigate({ to: "/user-not-activated" });
      return;
    }
    localStorage.setItem("is_active", "true");
    return response;
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    queryClient.clear();
    navigate({ to: "/login" });
  };

  return {
    signUpMutation,
    loginMutation,
    logout,
    checkIsActiveMutation,
    user,
    isLoadingUser,
    error,
    resetError: () => setError(null),
  };
};

export default useAuth;
