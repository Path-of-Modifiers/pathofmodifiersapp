import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import { useEffect } from "react";
import useCustomToast from "../useCustomToast";
import { findWinsorUpperBound } from "./utils";

/**
 * A hook that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function useGetPlotData(plotQuery: PlotQuery): {
  result: Datum[] | undefined;
  mostCommonCurrencyUsed: string | undefined;
  confidenceRating: "low" | "medium" | "high" | undefined;
  upperBoundryChaos: number;
  upperBoundrySecondary: number;
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
    // const cleanData: Datum[] = [];
    // const upperBoundryChaos = findWinsorUpperBound(plotData.valueInChaos);
    // const upperBoundrySecondary = findWinsorUpperBound(
    //   plotData.valueInMostCommonCurrencyUsed
    // );
    // for (let i = 0; i < plotData?.hoursSinceLaunch.length; i++) {
    //   cleanData.push({
    //     timestamp: plotData.hoursSinceLaunch[i],
    //     valueInChaos: plotData.valueInChaos[i],
    //     valueInMostCommonCurrencyUsed:
    //       plotData.valueInMostCommonCurrencyUsed[i],
    //     confidence: plotData.confidence[i],
    //   });
    // }
    // const data: Datum[] = cleanData.reduce((prev, curVal) => {
    //   if (prev.length === 0) {
    //     return [curVal];
    //   }
    //   const prevVal = prev[prev.length - 1];
    //   const hourGap = curVal.timestamp - prevVal.timestamp;
    //   if (hourGap > 1) {
    //     const gapFiller: Datum[] = [];
    //     for (let j = 0; j < hourGap; j++) {
    //       gapFiller.push({
    //         timestamp: prevVal.timestamp + j + 1,
    //         valueInChaos: null,
    //         valueInMostCommonCurrencyUsed: null,
    //         confidence: null,
    //       });
    //     }
    //     return [...prev, ...gapFiller, curVal];
    //   }
    //   return [...prev, curVal];
    // }, [] as Datum[]);
    return {
      result: data,
      mostCommonCurrencyUsed: plotData.mostCommonCurrencyUsed,
      confidenceRating: plotData.confidenceRating,
      upperBoundryChaos,
      upperBoundrySecondary,
      fetchStatus,
      error,
    };
  }
  return {
    result: undefined,
    mostCommonCurrencyUsed: undefined,
    confidenceRating: undefined,
    upperBoundryChaos: 0,
    upperBoundrySecondary: 0,
    fetchStatus,
    error,
  };
}

export default useGetPlotData;
