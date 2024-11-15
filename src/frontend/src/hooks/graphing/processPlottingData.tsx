import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import { useEffect } from "react";
import useCustomToast from "../useCustomToast";

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
  const { plotData, fetchStatus, isFetched, isError, error } =
    usePostPlottingData(plotQuery);

  const showToast = useCustomToast();

  useEffect(() => {
    if (isError && isFetched) {
      if (error != null) {
        showToast("Plotting error", error.message, "error");
      }
    }
  }, [isError, isFetched, error, showToast]);

  if (plotData !== undefined) {
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
