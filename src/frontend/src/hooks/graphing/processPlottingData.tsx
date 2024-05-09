import { QueryClient } from '@tanstack/query-core';
import { PostPlottingData } from "./postPlottingData";
import { PlotQuery } from "../../client";
import { groupByAndMeanTopN } from './utils';

interface Datum {
    xaxis: Date,
    yaxis1: number,
    yaxis2?: number
}

const plotQuery: PlotQuery = {
    league: "Standard",
    itemSpecifications: {
        identified: true
    },
    wantedModifiers: [
        {
            modifierId: 61,
            position: 1,
            modifierLimitations: {
                textRoll: 0
            }
        }
    ]
};

const testAPI = () => {
    const plotData = PostPlottingData(plotQuery)

    const data: Datum[] = []
    if (plotData?.timeStamp !== undefined) {
        for (let i = 0; i <plotData?.timeStamp.length; i++) {
            data.push({
                xaxis: new Date(plotData.timeStamp[i]),
                yaxis1: plotData.valueInChaos[i]
            })
        }
    }
    const result = groupByAndMeanTopN(data, 100);
    return result
};

export default testAPI;