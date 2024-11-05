import { useQueryClient } from "@tanstack/react-query";
import { ItemBaseTypesService, ItemBaseType } from "../../client";

// Fetches all item base type data and processes related unique item names
export const useGetItemBaseTypes = async () => {
    const queryClient = useQueryClient();

    try {
        // Fetch and return item base types directly
        const itemBaseTypes = await queryClient.fetchQuery({
            queryKey: ["baseTypeValues"],
            queryFn: async () => {
                const data = await ItemBaseTypesService.getAllItemBaseTypes({});
                return Array.isArray(data) ? data : [data];
            },
        });

        const createItemNameArray = (itemBaseType: ItemBaseType[]): string[] => {
            const reduceItemNameArray = (
                prev: string[] | undefined,
                cur: string[] | undefined
            ): string[] => {
                prev = prev || [];
                if (cur) {
                    const newItemNames = cur.filter((value) => !prev.includes(value));
                    prev.push(...newItemNames);
                }
                return prev;
            };

            const arrayOfRelatedUniques = itemBaseType.map((baseType) => {
                const relatedUniques = baseType.relatedUniques;
                return relatedUniques ? relatedUniques.split("|") : [];
            });

            return arrayOfRelatedUniques.reduce(reduceItemNameArray, []);
        };

        const itemNames = createItemNameArray(itemBaseTypes);

        return {
            itemBaseTypes,
            itemNames,
        };

    } catch (error) {
        console.error("Error fetching item base types:", error);
        return {
            itemBaseTypes: [],
            itemNames: [],
        };
    }
};

