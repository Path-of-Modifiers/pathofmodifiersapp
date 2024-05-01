import { useState } from "react";
import {PlottingService, PlotQuery, PlotData } from "../client";
import { useQuery } from "@tanstack/react-query";

const plotData: PlotData = {
  valueInChaos: [0, 1, 2, 3],
  timeStamp: ["2024-05-01T11:16:41.690Z", "2024-05-02T11:16:41.690Z", "2024-05-03T11:16:41.690Z", "2024-05-04T11:16:41.690Z"],
  mostCommonCurrencyUsed: "divine",
  conversionValue: [1, 1, 1, 1]
}

export const PostPlottingData = (requestBody: PlotQuery) => {
  const [responseBody, setPlotData] = useState<PlotData>(plotData);
  try {
    // setPlotData(plotData)
    // useQuery({
    //   queryKey: ["allPlotData"],
    //   queryFn: async () => {
    //     setPlotData(
    //       await PlottingService.getPlotDataApiApiV1PlotPost({requestBody})
    //     );
    //   },
    // });
    console.log(responseBody)
    return responseBody
  } catch (error) {
    console.log(error);
  }
};
