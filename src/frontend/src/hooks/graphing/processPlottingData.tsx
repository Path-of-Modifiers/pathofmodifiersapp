import { PostPlottingData } from "./postPlottingData";
import { PlotQuery } from "../../client";
import { groupByAndMeanTopN } from "./utils";
// import { useGraphInputStore } from "../../store/GraphInputStore";

interface Datum {
  date: string;
  valueInChaos: number;
  yaxis2?: number;
}

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
