import { useEffect, useState } from "react";
import {
  TurnstyleQuery,
  TurnstyleResponse,
  TurnstylesService,
} from "../../client";
import { useQuery } from "@tanstack/react-query";
import { useGraphInputStore } from "../../store/GraphInputStore";

/**
 * Posts the request body (a turnstyle query) and returns the
 * corresponding turnstyle response from the cloudflare verify challenge
 * endpoint.
 * @param requestBody The Plot Query
 * @returns The Plot Data or undefined if no query yet, and the fetch status
 */
function useTurnstyleValidation(requestBody: TurnstyleQuery): {
  turnstyleResponse: TurnstyleResponse | undefined;
  fetchStatus: string;
  isError: boolean;
  isFetched: boolean;
} {
  const [turnstyleResponse, setTurnstyleRespones] =
    useState<TurnstyleResponse>();
  const queryClicked = useGraphInputStore((state) => state.queryClicked);
  const { fetchStatus, refetch, isFetched, isError } = useQuery({
    queryKey: ["allTurnstyleData"],
    queryFn: async () => {
      const returnBody =
        await TurnstylesService.getTurnstyleValidationApiApiV1TurnstylePost({
          requestBody,
        });

      console.log("RETURNBODY TURNSTYLE", returnBody);

      setTurnstyleRespones(returnBody);
      return 1;
    },
    enabled: false, // stops constant refreshes
  });
  useEffect(() => {
    // Only refetches data if the query button is clicked
    if (queryClicked) {
      refetch();
    }
  }, [queryClicked, refetch]);
  return { turnstyleResponse, fetchStatus, isFetched, isError };
}

export default useTurnstyleValidation;
