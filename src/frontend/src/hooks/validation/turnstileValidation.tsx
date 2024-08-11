import { useQuery } from "@tanstack/react-query";
import {
  TurnstileQuery,
  TurnstileResponse,
  TurnstilesService,
} from "../../client";

export const hasCompletedCaptcha = () => {
  return localStorage.getItem("hasCompletedCaptcha") === "true";
};

/**
 * Posts the request body (a turnstile query) and returns the
 * corresponding turnstile response from the cloudflare verify challenge
 * endpoint.
 * @param requestBody The Plot Query
 * @returns The Plot Data or undefined if no query yet, and the fetch status
 */
function useTurnstileValidation(requestBody: TurnstileQuery): {
  turnstileResponse: TurnstileResponse | undefined;
  fetchStatus: string;
  isError: boolean;
  isFetched: boolean;
  isLoading: boolean;
} {
  const {
    data: turnstileResponse,
    status: fetchStatus,
    isError,
    isFetched,
    isLoading,
  } = useQuery({
    queryKey: ["allTurnstileData", requestBody], // Include requestBody to ensure it updates on changes
    queryFn: async () => {
      if (!requestBody || !requestBody.ip) {
        return undefined; // Return undefined if the request body is invalid
      }

      const returnBody = await TurnstilesService.getTurnstileValidation({
        requestBody,
      });
      if (returnBody.success) {
        localStorage.setItem("hasCompletedCaptcha", "true");
      }

      return returnBody; // Return the fetched data
    },
    enabled: !!requestBody && !!requestBody.token && !!requestBody.ip, // Only run the query if requestBody is valid
  });
  return { turnstileResponse, fetchStatus, isFetched, isError, isLoading };
}

export default useTurnstileValidation;
