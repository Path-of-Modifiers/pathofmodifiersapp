import usePostPlottingData from "./postPlottingData";
import { PlotQuery } from "../../client";
import Datum from "../../schemas/Datum";
import formatDateToLocal from "./utils";
import { useErrorStore } from "../../store/ErrorStore";
import { useEffect } from "react";

/**
 * A hook that takes the current plot query and returns
 * data that is ready to be plotted.
 * @returns The processed data or undefined and the current fetch status.
 */
function useGetPlotData(plotQuery: PlotQuery): {
    result: Datum[] | undefined;
    mostCommonCurrencyUsed: string | undefined;
    fetchStatus: string;
    isError: boolean;
} {
    const { leagueError, modifiersError, setResultError } =
        useErrorStore.getState();

    const { plotData, fetchStatus, isFetched, isError } =
        usePostPlottingData(plotQuery);

    useEffect(() => {
        if (isError && isFetched) {
            setResultError(true);
        } else {
            setResultError(false);
        }
    }, [isError, isFetched, setResultError]);

    if (isError || leagueError || modifiersError) {
        return {
            result: undefined,
            mostCommonCurrencyUsed: undefined,
            fetchStatus,
            isError: true,
        };
    } else if (plotData !== undefined) {
        const data: Datum[] = [];
        for (let i = 0; i < plotData?.timeStamp.length; i++) {
            data.push({
                date: formatDateToLocal(plotData.timeStamp[i]),
                valueInChaos: plotData.valueInChaos[i],
                valueInMostCommonCurrencyUsed:
                    plotData.valueInMostCommonCurrencyUsed[i],
            });
        }
        return {
            result: data,
            mostCommonCurrencyUsed: plotData.mostCommonCurrencyUsed,
            fetchStatus,
            isError: false,
        };
    } else {
        return {
            result: undefined,
            mostCommonCurrencyUsed: undefined,
            fetchStatus,
            isError: true,
        };
    }
}

export default useGetPlotData;
