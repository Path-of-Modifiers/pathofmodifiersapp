import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import { allValueInChaos } from "./utils";
import { useErrorStore } from "../../store/ErrorStore";

/**
 * A hook that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function useGetPlotData(plotQuery: PlotQuery): {
  result: Datum[] | undefined;
  fetchStatus: string;
} {
  const { plotData, fetchStatus } = usePostPlottingData(plotQuery);
  const leagueError = useErrorStore.getState().leagueError;
  const modifiersError = useErrorStore.getState().modifiersError;
  let result: Datum[] | undefined = undefined;

  if (
    plotData === undefined ||
    modifiersError === true ||
    leagueError === true
  ) {
    return { result, fetchStatus };
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
  return { result, fetchStatus };
}

export default useGetPlotData;
