import { useState } from "react";
import {
  TurnstileQuery,
  TurnstileResponse,
  TurnstilesService,
} from "../../client";
import { useQuery } from "@tanstack/react-query";

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
  const [turnstileResponse, setTurnstileRespones] =
      useState<TurnstileResponse | undefined>();
  const { fetchStatus, isFetched, isError } = useQuery({
    queryKey: ["allTurnstileData"],
    queryFn: async () => {
      if (!requestBody || !requestBody.token || !requestBody.ip) {
        return 0;
      }
      const returnBody =
        await TurnstilesService.getTurnstileValidationApiApiV1TurnstilePost({
          requestBody,
        });

      console.log("RETURNBODY TURNSTYLE", returnBody);

      setTurnstileRespones(returnBody);
      return 1;
    },
    enabled: false, // stops constant refreshes
  });
  return { turnstileResponse, fetchStatus, isFetched, isError };
}

export default useTurnstileValidation;
