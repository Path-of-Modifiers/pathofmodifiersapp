import PostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import { allValueInChaos } from "./utils";
/**
 * A function that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function GetPlotData(plotQuery: PlotQuery): {
  result: Datum[] | undefined;
  fetchStatus: string;
} {
  const { plotData, fetchStatus } = PostPlottingData(plotQuery);
  let result: Datum[] | undefined = undefined;
  if (plotData === undefined) {
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

export default GetPlotData;
