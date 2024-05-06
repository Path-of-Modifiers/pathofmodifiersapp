import { QueryClient } from "@tanstack/react-query";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
  ItemBaseTypesService,
} from "../client";

export const prefetchAllBaseTypeData = async (queryClient: QueryClient) => {
  let baseTypes: BaseType[] = [];
  let itemBaseTypeCategory: ItemBaseTypeCategory[] = [];
  let itemBaseTypeSubCategory: ItemBaseTypeSubCategory[] = [];

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

  return { baseTypes, itemBaseTypeCategory, itemBaseTypeSubCategory };
};
