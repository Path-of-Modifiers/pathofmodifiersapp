import { useMutation, useQuery } from "@tanstack/react-query";
import {
  ApiError,
  TemporaryHashedUserIpPrefixsService,
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

  const navigate = useNavigate();

  const { data: valid_ip_response, isLoading } = useQuery<
    boolean | null,
    Error
  >({
    queryKey: ["valid_ip_check", hasCompletedCaptcha()],
    queryFn: async () => {
      const ip = requestBody.ip;
      const response =
        await TemporaryHashedUserIpPrefixsService.checkTemporaryHashedUserIp({
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
  });

  const getTurnstileValidation = async (valid_ip_response: TurnstileQuery) => {
    const turnstileValidation = await TurnstilesService.getTurnstileValidation({
      requestBody: valid_ip_response,
    });

    localStorage.setItem(
      "hasCompletedCaptcha",
      turnstileValidation.success?.toString()
    );
  };

  const performTurnstileValidation = useMutation({
    mutationFn: getTurnstileValidation,

    onSuccess: () => {
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
    localStorage.removeItem("hasCompletedCaptcha");
    navigate({ to: "/captcha" });
  };

  return {
    performTurnstileValidation,
    valid_ip_response,
    logout,
    isLoading,
    error,
    resetError: () => setError(null),
  };
};

export default useTurnstileValidation;
