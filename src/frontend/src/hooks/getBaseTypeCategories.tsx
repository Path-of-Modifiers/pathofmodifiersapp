import { useState } from "react";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
  ItemBaseTypesService,
} from "../client";
import { useQuery } from "@tanstack/react-query";

export const GetBaseTypes = () => {
  const [baseTypes, setBaseTypes] = useState<BaseType | BaseType[]>([]);
  try {
    useQuery({
      queryKey: ["baseTypes"],
      queryFn: async () => {
        setBaseTypes(
          await ItemBaseTypesService.getBaseTypesApiApiV1ItemBaseTypeBaseTypesGet()
        );
      },
    });
    if (Array.isArray(baseTypes)) {
      return baseTypes; // If modifiers is already an array, return it directly
    } else {
      return [baseTypes]; // If modifiers is not an array, wrap it in an array
    }
  } catch (error) {
    console.log(error);
  }
};

export const GetItemBaseTypeCategories = () => {
  const [itemBaseTypeCategory, setItemBaseTypeCategory] = useState<
    ItemBaseTypeCategory | ItemBaseTypeCategory[]
  >([]);
  try {
    useQuery({
      queryKey: ["itemBaseTypeCategory"],
      queryFn: async () => {
        setItemBaseTypeCategory(
          await ItemBaseTypesService.getUniqueCategoriesApiApiV1ItemBaseTypeUniqueCategoriesGet()
        );
      },
    });
    if (Array.isArray(itemBaseTypeCategory)) {
      return itemBaseTypeCategory; // If modifiers is already an array, return it directly
    } else {
      return [itemBaseTypeCategory]; // If modifiers is not an array, wrap it in an array
    }
  } catch (error) {
    console.log(error);
  }
};

export const GetItemBaseTypeSubCategories = () => {
  const [itemBaseTypeSubCategory, setItemBaseTypeSubCategory] = useState<
    ItemBaseTypeSubCategory | ItemBaseTypeSubCategory[]
  >([]);
  try {
    useQuery({
      queryKey: ["itemBaseTypeSubCategory"],
      queryFn: async () => {
        setItemBaseTypeSubCategory(
          await ItemBaseTypesService.getUniqueSubCategoriesApiApiV1ItemBaseTypeUniqueSubCategoriesGet()
        );
      },
    });
    if (Array.isArray(itemBaseTypeSubCategory)) {
      return itemBaseTypeSubCategory; // If modifiers is already an array, return it directly
    } else {
      return [itemBaseTypeSubCategory]; // If modifiers is not an array, wrap it in an array
    }
  } catch (error) {
    console.log(error);
  }
};
