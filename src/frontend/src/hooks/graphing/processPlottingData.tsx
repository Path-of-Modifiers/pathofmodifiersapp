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
  error: Error | null;
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
    const data1: Datum[] = [];
    for (let i = 0; i < plotData?.hoursSinceLaunch.length; i++) {
      data1.push({
        timestamp: plotData.hoursSinceLaunch[i],
        valueInChaos: plotData.valueInChaos[i],
        valueInMostCommonCurrencyUsed:
          plotData.valueInMostCommonCurrencyUsed[i],
        confidence: plotData.confidence[i],
      });
    }
    const data: Datum[] = data1.reduce((prev, curVal) => {
      if (prev.length === 0) {
        return [curVal];
      }
      const prevVal = prev[prev.length - 1];
      const hourGap = curVal.timestamp - prevVal.timestamp;
      if (hourGap > 1) {
        const gapFiller: Datum[] = [];
        for (let j = 0; j < hourGap; j++) {
          gapFiller.push({
            timestamp: prevVal.timestamp + j + 1,
            valueInChaos: null,
            valueInMostCommonCurrencyUsed: null,
            confidence: null,
          });
        }
        return [...prev, ...gapFiller, curVal];
      }
      return [...prev, curVal];
    }, [] as Datum[]);

    return {
      result: data,
      mostCommonCurrencyUsed: plotData.mostCommonCurrencyUsed,
      confidenceRating: plotData.confidenceRating,
      fetchStatus,
      error,
    };
  }
  return {
    result: undefined,
    mostCommonCurrencyUsed: undefined,
    confidenceRating: undefined,
    fetchStatus,
    error,
  };
}

export default useGetPlotData;
