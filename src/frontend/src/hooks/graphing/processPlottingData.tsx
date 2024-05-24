import PostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import { groupByAndMeanTopN } from "./utils";
import Datum from "../../schemas/Datum";
/**
 * A function that takes the current plot query and returns
 * data that is ready to be plotted.
 *
 * The data retrieved from the database is grouped by the hour
 * and only the cheapest 100 items that hour are considered.
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
  result = groupByAndMeanTopN(data, 100);
  return { result, fetchStatus };
}

export default GetPlotData;
