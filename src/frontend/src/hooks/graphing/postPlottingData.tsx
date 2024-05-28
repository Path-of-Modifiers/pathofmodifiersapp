import { useEffect, useState } from "react";
import { PlottingService, PlotQuery, PlotData } from "../../client";
import { useQuery } from "@tanstack/react-query";
import { useGraphInputStore } from "../../store/GraphInputStore";

/**
 * Posts the request body (a plot query) and returns the
 * corresponding plot data from the data base.
 * @param requestBody The Plot Query
 * @returns The Plot Data or undefined if no query yet, and the fetch status
 */
function PostPlottingData(requestBody: PlotQuery): {
  plotData: PlotData | undefined;
  fetchStatus: string;
} {
  const [plotData, setPlotData] = useState<PlotData>();
  const queryClicked = useGraphInputStore((state) => state.queryClicked);
  const { fetchStatus, refetch } = useQuery({
    queryKey: ["allPlotData"],
    queryFn: async () => {
      const returnBody = await PlottingService.getPlotDataApiApiV1PlotPost({
        requestBody,
      });

      setPlotData(returnBody);
      return 1;
    },
    enabled: false, // stops constant refreshes
  });
  useEffect(() => {
    // Only refetches data if the query button is clicked
    if (queryClicked) {
      refetch();
    }
  }, [queryClicked, refetch]);
  return { plotData, fetchStatus };
}

export default PostPlottingData;
