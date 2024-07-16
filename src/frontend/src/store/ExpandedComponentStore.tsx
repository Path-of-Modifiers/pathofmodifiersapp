import { create } from "zustand";
import { ExpandedComponentState } from "./StateInterface";

export const useExpandedComponentStore = create<ExpandedComponentState>(
  (set) => ({
    expandedGraphInputFilters: false,

    setExpandedGraphInputFilters: (expandedGraphInputFilters: boolean) =>
      set(() => ({ expandedGraphInputFilters: expandedGraphInputFilters })),
  })
);
