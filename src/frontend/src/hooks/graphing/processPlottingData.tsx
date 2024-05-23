import { PostPlottingData } from "./postPlottingData";
import { PlotQuery } from "../../client";
import { groupByAndMeanTopN } from "./utils";
import Datum from "../../schemas/Datum";
// import { useGraphInputStore } from "../../store/GraphInputStore";

// Will remove when the we hook up the user input
const plotQuery: PlotQuery = {
  league: "Necropolis",
  itemSpecifications: {
    identified: true,
  },
  wantedModifiers: [
    {
      modifierId: 61,
      position: 1,
      modifierLimitations: {
        textRoll: 0,
      },
    },
  ],
};
/**
 * A function that takes the current plot query and returns
 * data that is ready to be plotted.
 *
 * The data retrieved from the database is grouped by the hour
 * and only the cheapest 100 items that hour are considered.
 * @returns result
 */
const getPlotData = () => {
  const plotData = PostPlottingData(plotQuery);

  const data: Datum[] = [];
  if (plotData?.timeStamp !== undefined) {
    for (let i = 0; i < plotData?.timeStamp.length; i++) {
      data.push({
        date: plotData.timeStamp[i],
        valueInChaos: plotData.valueInChaos[i],
      });
    }
  }
  const result = groupByAndMeanTopN(data, 100);
  return result;
};

export default getPlotData;
