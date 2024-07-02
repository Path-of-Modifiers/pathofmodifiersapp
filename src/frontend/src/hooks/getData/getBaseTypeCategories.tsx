import { QueryClient } from "@tanstack/react-query";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
  ItemBaseTypesService,
} from "../../client";

// Prefetches all item base type data
export const prefetchAllBaseTypeData = async (queryClient: QueryClient) => {
  let baseTypes: BaseType[] = [];
  let itemBaseTypeCategory: ItemBaseTypeCategory[] = [];
  let itemBaseTypeSubCategory: ItemBaseTypeSubCategory[] = [];
  try {
    // Prefetch all base type data
    await queryClient.prefetchQuery({
      queryKey: ["baseTypes"],
      queryFn: async () => {
        const data =
          await ItemBaseTypesService.getBaseTypesApiApiV1ItemBaseTypeBaseTypesGet();
        if (Array.isArray(data)) {
          baseTypes = data;
        } else {
          baseTypes = [data];
        }
        return 1;
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    // Prefetch all unique categories
    await queryClient.prefetchQuery({
      queryKey: ["itemBaseTypeCategory"],
      queryFn: async () => {
        const data =
          await ItemBaseTypesService.getUniqueCategoriesApiApiV1ItemBaseTypeUniqueCategoriesGet();
        if (Array.isArray(data)) {
          itemBaseTypeCategory = data;
        } else {
          itemBaseTypeCategory = [data];
        }
        return 1;
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });

    // Prefetch all unique sub categories
    await queryClient.prefetchQuery({
      queryKey: ["itemBaseTypeSubCategory"],
      queryFn: async () => {
        const data =
          await ItemBaseTypesService.getUniqueSubCategoriesApiApiV1ItemBaseTypeUniqueSubCategoriesGet();
        if (Array.isArray(data)) {
          itemBaseTypeSubCategory = data;
        } else {
          itemBaseTypeSubCategory = [data];
        }
        return 1;
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });
  } catch (error) {
    console.log(error);
  }

  return { baseTypes, itemBaseTypeCategory, itemBaseTypeSubCategory };
};
