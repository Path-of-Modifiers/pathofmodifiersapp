import { useState } from "react";
import {PlottingService, PlotQuery, PlotData } from "../client";
import { useQuery } from "@tanstack/react-query";

export const PostPlottingData = (requestBody: PlotQuery) => {
  const [responseBody, setPlotData] = useState<PlotData>();
  try {
    useQuery({
      queryKey: ["allModifiers"],
      queryFn: async () => {
        setPlotData(
          await PlottingService.getPlotDataApiApiV1PlotPost({requestBody})
        );
      },
    });
    return responseBody
  } catch (error) {
    console.log(error);
  }
};
