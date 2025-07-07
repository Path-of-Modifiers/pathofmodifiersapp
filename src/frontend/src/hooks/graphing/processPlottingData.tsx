import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import { FilledPlotData } from "../../schemas/Datum";
import { useEffect } from "react";
import useCustomToast from "../useCustomToast";
import { findWinsorUpperBound, getHoursSinceLaunch } from "./utils";
import { PLOTTING_WINDOW_HOURS } from "../../config";

/**
 * A hook that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function useGetPlotData(plotQuery: PlotQuery): {
  result: FilledPlotData | undefined;
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
    const mostCommonCurrencyUsed = plotData.mostCommonCurrencyUsed;
    const currentHour = getHoursSinceLaunch(new Date());
    const firstHour = currentHour - PLOTTING_WINDOW_HOURS;
    const filledPlotData: FilledPlotData = {
      mostCommonCurrencyUsed: mostCommonCurrencyUsed,
      data: plotData.data.map(
        (val) => (
          {
            confidenceRating: val.confidenceRating,
            name: val.name,
            data: []
          }))
    };
    const currentIdxArray = plotData.data.reduce((prev, cur) => [...prev, 0], [] as number[]);
    let currentIdx: number;
    // Makes a filled plot data object, meaning that every hour has an entry
    // Missing entries from the original plot data is replaced by a "null" entry
    for (let hour = firstHour; hour <= currentHour; hour++) {
      for (let seriesIdx = 0; seriesIdx < currentIdxArray.length; seriesIdx++) {
        currentIdx = currentIdxArray[seriesIdx];
        if (
          plotData.data[seriesIdx].data.length <= currentIdx ||
          plotData.data[seriesIdx].data[currentIdx].hoursSinceLaunch !== hour
        ) {
          filledPlotData.data[seriesIdx].data.push(
            {
              hoursSinceLaunch: hour,
              valueInChaos: null,
              valueInMostCommonCurrencyUsed: null,
              confidence: null
            })
        } else {
          filledPlotData.data[seriesIdx].data.push(
            plotData.data[seriesIdx].data[currentIdx]
          );
          currentIdxArray[seriesIdx] = currentIdx + 1;
        }
      }
    }
    const upperBoundryChaos = findWinsorUpperBound(
      plotData.data[0].data.reduce(
        (prev, cur) => [...prev, cur.valueInChaos],
        [] as number[]
      )
    );
    const upperBoundrySecondary = findWinsorUpperBound(
      plotData.data[0].data.reduce(
        (prev, cur) => [...prev, cur.valueInMostCommonCurrencyUsed],
        [] as number[]
      )
    );
    const confidenceRating = plotData.data[0].confidenceRating;
    return {
      result: filledPlotData,
      mostCommonCurrencyUsed,
      confidenceRating,
      upperBoundryChaos,
      upperBoundrySecondary,
      fetchStatus,
      error
    }
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
