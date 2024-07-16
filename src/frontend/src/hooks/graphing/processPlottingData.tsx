import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import { allValueInChaos } from "./utils";
import { useErrorStore } from "../../store/ErrorStore";
import { useEffect } from "react";

/**
 * A hook that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function useGetPlotData(plotQuery: PlotQuery): {
  result: Datum[] | undefined;
  fetchStatus: string;
  isError: boolean;
} {
  const { leagueError, modifiersError, setResultError } =
    useErrorStore.getState();
  const { plotData, fetchStatus, isFetched, isError } =
    usePostPlottingData(plotQuery);

  let result: Datum[] | undefined = undefined;

  useEffect(() => {
    if (isError && isFetched) {
      setResultError(true);
    } else {
      setResultError(false);
    }
  }, [isError, isFetched, setResultError]);

  if (isError || leagueError || modifiersError) {
    return { result, fetchStatus, isError: true };
  }
  const data: Datum[] = [];
  if (plotData?.timeStamp !== undefined) {
    for (let i = 0; i < plotData?.timeStamp.length; i++) {
      data.push({
        date: plotData.timeStamp[i],
        valueInChaos: plotData.valueInChaos[i],
      });
    }
  }
  result = allValueInChaos(data, 1);
  return { result, fetchStatus, isError: false };
}

export default useGetPlotData;
