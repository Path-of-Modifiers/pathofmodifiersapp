import { Box } from "@chakra-ui/react";
import { PlotQuery } from "../../client";
import { PostPlottingData } from "../../hooks/postPlottingData";

const plotQuery: PlotQuery = {
    league: "Standard",
    itemSpecifications: {
        identified: true
    },
    baseSpecifications: {
        baseType: "Timeless Jewel"
    },
    wantedModifiers: [
        {
            modifierId: 60,
            position: 0
        }
    ]
};

export const Plot = () => {
    const response = PostPlottingData(plotQuery)
    console.log("hey")
    console.log(plotQuery)
    console.log(response)
    return <Box p={5} />
}