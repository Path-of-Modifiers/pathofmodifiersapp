import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import formatHoursSinceLaunch from "./utils";
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

  const data: Datum[] = [];
  if (plotData !== undefined) {
    for (let i = 0; i < plotData?.hoursSinceLaunch.length; i++) {
      data.push({
        timestamp: formatHoursSinceLaunch(plotData.hoursSinceLaunch[i]),
        valueInChaos: plotData.valueInChaos[i],
        valueInMostCommonCurrencyUsed:
          plotData.valueInMostCommonCurrencyUsed[i],
      });
    }
    return {
      result: data,
      mostCommonCurrencyUsed: plotData.mostCommonCurrencyUsed,
      fetchStatus,
      error,
    };
  }
  return {
    result: undefined,
    mostCommonCurrencyUsed: undefined,
    fetchStatus,
    error,
  };
}

export default useGetPlotData;
