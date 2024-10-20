import { QueryClient } from "@tanstack/react-query";
import { ItemBaseTypesService, ItemBaseType } from "../../client";

// Prefetches all item base type data
export const prefetchAllBaseTypeData = async (queryClient: QueryClient) => {
  let itemBaseTypes: ItemBaseType[] = [];

  try {
    // Prefetch all unique values
    await queryClient.prefetchQuery({
      queryKey: ["uniqueBasetypeValues"],
      queryFn: async () => {
        const data = await ItemBaseTypesService.getAllItemBaseTypes();

        if (Array.isArray(data)) {
          itemBaseTypes = data;
        } else {
          itemBaseTypes = [data];
        }

        return 1;
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });
  } catch (error) {
    console.log(error);
  }
  const createUniqueArray = (itemBaseType: ItemBaseType[]) => {
    const reduceUniqueArray = (
      prev: string[] | undefined,
      cur: string[] | undefined
    ): string[] => {
      if (prev === undefined) {
        prev = [];
      }
      if (cur === undefined) {
        return prev;
      }
      const newUniques = cur.filter((value) => !prev.includes(value));
      prev.push(...newUniques);
      return prev;
    };

    const arrayOfUniques = itemBaseType.map((baseType) => {
      const relatedUniques = baseType.relatedUniques;
      if (relatedUniques) {
        return relatedUniques.split("|");
      }
      return [];
    });
    const uniques = arrayOfUniques.reduce(reduceUniqueArray, []);
    return uniques;
  };

  const uniques = createUniqueArray(itemBaseTypes);

  return {
    itemBaseTypes,
    uniques,
  };
};
