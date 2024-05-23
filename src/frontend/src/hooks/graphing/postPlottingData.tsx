import { useState } from "react";
import { PlottingService, PlotQuery, PlotData } from "../../client";
import { useQuery } from "@tanstack/react-query";

export const PostPlottingData = (requestBody: PlotQuery) => {
  const [responseBody, setPlotData] = useState<PlotData>();
  try {
    useQuery({
      queryKey: ["allPlotData"],
      queryFn: async () => {
        const returnBody = await PlottingService.getPlotDataApiApiV1PlotPost({
          requestBody,
        });

        setPlotData(returnBody);
        return 1;
      },
    });
    return responseBody;
  } catch (error) {
    console.log(error);
  }
};
