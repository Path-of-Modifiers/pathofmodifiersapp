import { useQuery } from "@tanstack/react-query";
import {
  TurnstileQuery,
  TurnstileResponse,
  TurnstilesService,
} from "../../client";

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
} {
  const {
    data: turnstileResponse,
    status: fetchStatus,
    isError,
    isFetched,
  } = useQuery({
    queryKey: ["allTurnstileData", requestBody], // Include requestBody to ensure it updates on changes
    queryFn: async () => {
      if (!requestBody || !requestBody.token || !requestBody.ip) {
        return undefined; // Return undefined if the request body is invalid
      }

      const returnBody =
        await TurnstilesService.getTurnstileValidationApiApiV1TurnstilePost({
          requestBody,
        });

      return returnBody; // Return the fetched data
    },
    enabled: !!requestBody && !!requestBody.token && !!requestBody.ip, // Only run the query if requestBody is valid
  });
  return { turnstileResponse, fetchStatus, isFetched, isError };
}

export default useTurnstileValidation;
