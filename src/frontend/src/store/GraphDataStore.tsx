import { create } from "zustand";
import { GraphDataState } from "./StateInterface";
import {
  BaseType,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../client";

// Graph Data Store  -  This store is used to store graph data.
export const useGraphDataStore = create<GraphDataState>((set) => ({
  baseTypes: [],
  itemBaseTypeCategories: [],
  itemBaseTypeSubCategories: [],

  setBaseTypes: (baseTypes: BaseType[]) =>
    set(() => ({ baseTypes: baseTypes })),

  setItemBaseTypeCategories: (itemBaseTypeCategories: ItemBaseTypeCategory[]) =>
    set(() => ({ itemBaseTypeCategories: itemBaseTypeCategories })),

  setItemBaseTypeSubCategories: (
    itemBaseTypeSubCategories: ItemBaseTypeSubCategory[]
  ) => set(() => ({ itemBaseTypeSubCategories: itemBaseTypeSubCategories })),
}));
