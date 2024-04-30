import { Box } from "@chakra-ui/react";
import { PlotQuery } from "../../client";
import { PostPlottingData } from "../../hooks/postPlottingData";

const plotQuery: PlotQuery = {
    "league": "Standard",
    "itemSpecifications": {
        "identified": true
    },
    baseSpecifications: {
        "category": "jewel"
    },
    wantedModifiers: [
        {
            "modifierId": 0,
            "position": 0
        }
    ]

}
const response = PostPlottingData(plotQuery)

export const Plot = () => {
    // console.log("hey")
    // console.log("hey")
    // console.log("hey")
    // console.log("hey")
    // console.log("hey")
    console.log(response)
    return <Box p={5} />
}