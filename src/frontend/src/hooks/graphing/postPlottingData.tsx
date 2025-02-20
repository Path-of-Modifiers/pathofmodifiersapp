import { useEffect, useState } from "react";
import { PlotsService, PlotQuery, PlotData } from "../../client";
import { useQuery } from "@tanstack/react-query";
import { useGraphInputStore } from "../../store/GraphInputStore";

/**
 * Posts the request body (a plot query) and returns the
 * corresponding plot data from the data base.
 * @param plotQuery The Plot Query
 * @returns The Plot Data or undefined if no query yet, and the fetch status
 */
function usePostPlottingData(plotQuery: PlotQuery): {
  plotData: PlotData | undefined;
  fetchStatus: string;
  isError: boolean;
  isFetched: boolean;
  error: Error | null;
} {
  const [plotData, setPlotData] = useState<PlotData>();
  const { queryClicked } = useGraphInputStore();
  const { setFetchStatus } = useGraphInputStore();
  const { fetchStatus, refetch, isFetched, isError, error } = useQuery({
    queryKey: ["allPlotData"],
    queryFn: async () => {
      const returnBody = await PlotsService.getPlotData({
        requestBody: plotQuery,
      });

      setPlotData(returnBody);
      return 1;
    },
    retry: false,
    enabled: false, // stops constant refreshes
  });

  useEffect(() => {
    // Only refetches data if the query button is clicked
    setFetchStatus(fetchStatus);
    if (queryClicked && fetchStatus === "idle") {
      refetch();
    }
  }, [queryClicked, refetch, fetchStatus, setFetchStatus, plotQuery]);
  return { plotData, fetchStatus, isFetched, isError, error };
}

export default usePostPlottingData;
