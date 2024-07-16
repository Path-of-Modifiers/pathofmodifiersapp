import { create } from "zustand";
import { ExpandedComponentState } from "./StateInterface";

export const useExpandedComponentStore = create<ExpandedComponentState>(
  (set) => ({
    expandedGraphInputFilters: true,
    expandedModifiers: true,
    expandedBaseType: false,
    expandedMiscItem: false,

    setExpandedGraphInputFilters: (expandedGraphInputFilters: boolean) =>
      set(() => ({ expandedGraphInputFilters: expandedGraphInputFilters })),

    setExpandedModifiers: (expandedModifiers: boolean) =>
      set(() => ({ expandedModifiers: expandedModifiers })),

    setExpandedBaseType: (expandedBaseType: boolean) =>
      set(() => ({ expandedBaseType: expandedBaseType })),

    setExpandedMiscItem: (expandedMiscItem: boolean) =>
      set(() => ({ expandedMiscItem: expandedMiscItem })),
  })
);
