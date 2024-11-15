import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import { useErrorStore } from "../../store/ErrorStore";
import { useEffect } from "react";

/**
 * A hook that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function useGetPlotData(plotQuery: PlotQuery): {
  result: Datum[] | undefined;
  mostCommonCurrencyUsed: string | undefined;
  confidenceRating: "low" | "medium" | "high" | undefined;
  fetchStatus: string;
  isError: boolean;
} {
  const { leagueError, modifiersError, setResultError } =
    useErrorStore.getState();

  const { plotData, fetchStatus, isFetched, isError } =
    usePostPlottingData(plotQuery);

  useEffect(() => {
    if (isError && isFetched) {
      setResultError(true);
    } else {
      setResultError(false);
    }
  }, [isError, isFetched, setResultError]);

  if (isError || leagueError || modifiersError) {
    return {
      result: undefined,
      mostCommonCurrencyUsed: undefined,
      confidenceRating: undefined,
      fetchStatus,
      isError: true,
    };
  } else if (plotData !== undefined) {
    const data: Datum[] = [];
    for (let i = 0; i < plotData?.hoursSinceLaunch.length; i++) {
      data.push({
        timestamp: plotData.hoursSinceLaunch[i],
        valueInChaos: plotData.valueInChaos[i],
        valueInMostCommonCurrencyUsed:
          plotData.valueInMostCommonCurrencyUsed[i],
        confidence: plotData.confidence[i],
      });
    }
    return {
      result: data,
      mostCommonCurrencyUsed: plotData.mostCommonCurrencyUsed,
      confidenceRating: plotData.confidenceRating,
      fetchStatus,
      isError: false,
    };
  } else {
    return {
      result: undefined,
      mostCommonCurrencyUsed: undefined,
      confidenceRating: undefined,
      fetchStatus,
      isError: true,
    };
  }
}

export default useGetPlotData;
