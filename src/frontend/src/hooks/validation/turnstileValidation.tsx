import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ApiError,
  TemporaryHashedUserIpsService,
  TurnstileQuery,
  TurnstilesService,
} from "../../client";
import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { AxiosError } from "axios";

export const hasCompletedCaptcha = () => {
  return localStorage.getItem("hasCompletedCaptcha") !== null;
};

/**
 * Posts the request body (a turnstile query) and returns the
 * corresponding turnstile response from the cloudflare verify challenge
 * endpoint.
 * @param requestBody The Plot Query
 * @returns The Plot valid_ip_response or undefined if no query yet, and the fetch status
 */
const useTurnstileValidation = (requestBody: TurnstileQuery) => {
  const [error, setError] = useState<string | null>(null);
  const searchParams = new URLSearchParams(window.location.search);
  const from = searchParams.get("from");

  const navigate = useNavigate();

  const {
    data: valid_ip_response,
    isLoading: isLoadingCaptcha,
    isError,
  } = useQuery<boolean | null, Error>({
    queryKey: ["valid_ip_check", hasCompletedCaptcha()],
    queryFn: async () => {
      const ip = requestBody.ip;
      const response =
        await TemporaryHashedUserIpsService.checkTemporaryHashedUserIp({
          ip,
        });

      if (response) {
        localStorage.setItem("hasCompletedCaptcha", response.toString());
      } else {
        localStorage.removeItem("hasCompletedCaptcha");
        navigate({ to: "/captcha" });
      }

      return response;
    },
    retry: false,
  });

  if (isError) {
    localStorage.removeItem("hasCompletedCaptcha");
    navigate({ to: "/captcha" });
  }

  const completeCaptcha = async (data: TurnstileQuery) => {
    console.log("Completing captcha...");
    const response = await TurnstilesService.getTurnstileValidation({
      requestBody: data,
    });
    localStorage.setItem("hasCompletedCaptcha", response.success.toString());
  };

  const performTurnstileValidation = useMutation({
    mutationFn: completeCaptcha,

    onSuccess: () => {
      navigate({ to: from ? "/" + `${from}` : "/" });
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
    retry: false,
  });

  return {
    performTurnstileValidation,
    valid_ip_response,
    isLoadingCaptcha,
    error,
    resetError: () => setError(null),
  };
};

export default useTurnstileValidation;
