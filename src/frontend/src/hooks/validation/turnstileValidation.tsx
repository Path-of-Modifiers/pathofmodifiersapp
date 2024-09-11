import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ApiError,
  TurnstileQuery,
  TurnstileResponse,
  TurnstilesService,
} from "../../client";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AxiosError } from "axios";
import { isLoggedIn } from "./useAuth";
import useGetIp from "./getIp";

export const hasCompletedCaptcha = () => {
  return localStorage.getItem("turnstile_captcha_token") !== null;
};

/**
 * Posts the request body (a turnstile query) and returns the
 * corresponding turnstile response from the cloudflare verify challenge
 * endpoint.
 * @returns The turnstile response and the fetch status
 */
const useTurnstileValidation = (requestBody?: TurnstileQuery) => {
  const [token, setToken] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const searchParams = new URLSearchParams(window.location.search);
  const from = searchParams.get("from");
  const ip = useGetIp();

  const navigate = useNavigate();

  const {
    data: turnstileResponse,
    isLoading: isLoadingTurnstile,
    isError: isErrorTurnstile,
    isSuccess: isSuccessTurnstile,
  } = useQuery<TurnstileResponse | null, Error>({
    queryKey: ["turnstile", hasCompletedCaptcha(), isLoggedIn()],
    queryFn: async (): Promise<TurnstileResponse | null> => {
      const turnstileResponse = await TurnstilesService.getTurnstileValidation({
        requestBody: {
          token: requestBody?.token ?? token,
          ip: requestBody?.ip ?? ip,
        },
      });

      return turnstileResponse;
    },
    retry: false,
    enabled: isLoggedIn(),
  });

  if (!isLoggedIn() && isErrorTurnstile) {
    localStorage.removeItem("turnstile_captcha_token");
  }

  if (isSuccessTurnstile && turnstileResponse?.success) {
    setToken(requestBody?.token ?? "");
    if (requestBody?.token) {
      localStorage.setItem("turnstile_captcha_token", requestBody.token);
    }
    if (!isLoggedIn()) {
      navigate({ to: from ? "/" + `${from}` : "/login" });
    }
  }

  const completeCaptcha = async (data: TurnstileQuery) => {
    console.log("Completing captcha...");
    await TurnstilesService.getTurnstileValidation({
      requestBody: data,
    });
  };

  const performTurnstileValidation = useMutation({
    mutationFn: completeCaptcha,

    onSuccess: () => {
      setToken(requestBody?.token ?? "");
      localStorage.setItem(
        "turnstile_captcha_token",
        requestBody?.token ?? token
      );
      navigate({ to: from ? "/" + `${from}` : "/" });
    },

    onError: (err: ApiError) => {
      localStorage.removeItem("turnstile_captcha_token");
      let errDetail = err.body?.detail;

      if (err instanceof AxiosError) {
        errDetail = err.message;
      }

      if (Array.isArray(errDetail)) {
        errDetail = "Something went wrong";
      }

      setError(errDetail);
    },
    retry: false,
  });

  return {
    performTurnstileValidation,
    isLoadingTurnstile,
    isErrorTurnstile,
    error,
    resetError: () => setError(null),
  };
};

export default useTurnstileValidation;
