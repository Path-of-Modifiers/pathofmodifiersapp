import { useEffect, useState } from "react";
import { PlotsService, PlotQuery, PlotData } from "../../client";
import { useQuery } from "@tanstack/react-query";
import { useGraphInputStore } from "../../store/GraphInputStore";
import type { BaseSpecs } from "../../client/models/BaseSpecs";
import type { ItemSpecs } from "../../client/models/ItemSpecs";
import { BaseSpecState } from "../../store/StateInterface";
import { useErrorStore } from "../../store/ErrorStore";

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
} {
    const [localPlotQuery, setLocalPlotQuery] = useState<PlotQuery>();
    const [plotData, setPlotData] = useState<PlotData>();
    const {
        queryClicked,
        wantedModifierExtended,
        itemName,
        choosableItemBaseType,
    } = useGraphInputStore();
    const {
        setNoRelatedUniqueError,
        setItemDoesNotHaveSelectedModifiersError,
        setBaseSpecDoesNotMatchError,
    } = useErrorStore();
    const { setFetchStatus } = useGraphInputStore();
    const { fetchStatus, refetch, isFetched, isError } = useQuery({
        queryKey: ["allPlotData"],
        queryFn: async () => {
            if (localPlotQuery == null) {
                return 0;
            }
            const returnBody = await PlotsService.getPlotData({
                requestBody: localPlotQuery,
            });

            setPlotData(returnBody);
            return 1;
        },
        retry: false,
        enabled: false, // stops constant refreshes
    });

    useEffect(() => {
        const handleQueryClicked = () => {
            // currently always runs, needs to be in if check
            // when Non-unique rarity is possible
            let itemSpec: ItemSpecs | undefined | null =
                plotQuery.itemSpecifications;
            let baseSpec: BaseSpecs | undefined | null =
                plotQuery.baseSpecifications;
            let possibleUniques = wantedModifierExtended.reduce(
                (prev, cur, index) => {
                    if (cur.relatedUniques === undefined || !cur.isSelected) {
                        return prev;
                    }

                    const newUniqueCandidates = cur.relatedUniques.split("|");
                    if (index === 0) {
                        return newUniqueCandidates;
                    }
                    return prev.filter((prevCandidate) =>
                        newUniqueCandidates.includes(prevCandidate)
                    );
                },
                [] as string[]
            );
            if (possibleUniques.length === 0) {
                setNoRelatedUniqueError(true);
                return;
            } else {
                setNoRelatedUniqueError(false);
            }
            if (itemName != null) {
                if (!possibleUniques.includes(itemName)) {
                    setItemDoesNotHaveSelectedModifiersError(true);
                    return;
                } else {
                    setItemDoesNotHaveSelectedModifiersError(false);
                }
                possibleUniques = [itemName];
            }
            // Only applicable if rarity is unique and base spec is not already
            // chosen
            const possibleBaseSpecs = choosableItemBaseType.reduce(
                (prev, cur) => {
                    if (cur.relatedUniques == null) {
                        return prev;
                    }
                    const relatedUniques = cur.relatedUniques.split("|");
                    if (
                        possibleUniques.some((unique) =>
                            relatedUniques.includes(unique)
                        )
                    ) {
                        if (
                            !baseSpec ||
                            ((!baseSpec.baseType ||
                                baseSpec.baseType === cur.baseType) &&
                                (!baseSpec.category ||
                                    baseSpec.category === cur.category) &&
                                (!baseSpec.subCategory ||
                                    baseSpec.subCategory === cur.subCategory))
                        ) {
                            return [
                                ...prev,
                                {
                                    baseType: cur.baseType,
                                    category: cur.category,
                                    subCategory: cur.subCategory,
                                },
                            ];
                        }
                    }
                    return prev;
                },
                [] as BaseSpecState[]
            );

            if (possibleBaseSpecs.length === 0) {
                setBaseSpecDoesNotMatchError(true);
                return;
            } else {
                setBaseSpecDoesNotMatchError(false);
            }
            if (baseSpec != null) {
                if (possibleBaseSpecs.length === 1) {
                    baseSpec = possibleBaseSpecs[0];
                }
            }

            itemSpec = { ...itemSpec, name: possibleUniques.join("|") };
            setLocalPlotQuery({
                league: plotQuery.league,
                itemSpecifications: itemSpec,
                baseSpecifications: baseSpec,
                wantedModifiers: plotQuery.wantedModifiers,
            });
            refetch();
        };
        // Only refetches data if the query button is clicked
        setFetchStatus(fetchStatus);
        if (queryClicked) {
            handleQueryClicked();
        }
    }, [
        queryClicked,
        refetch,
        fetchStatus,
        setFetchStatus,
        plotQuery.itemSpecifications,
        plotQuery.baseSpecifications,
        wantedModifierExtended,
        itemName,
        localPlotQuery,
        setNoRelatedUniqueError,
        setItemDoesNotHaveSelectedModifiersError,
        choosableItemBaseType,
        plotQuery,
        setBaseSpecDoesNotMatchError,
    ]);
    return { plotData, fetchStatus, isFetched, isError };
}

export default usePostPlottingData;
