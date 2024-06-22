import { create } from "zustand";
import { ExpandedComponentState } from "./StateInterface";

export const useExpandedComponentStore = create<ExpandedComponentState>(
  (set) => ({
    expandedGraphInputFilters: true,

    setExpandedGraphInputFilters: (expandedGraphInputFilters: boolean) =>
      set(() => ({ expandedGraphInputFilters: expandedGraphInputFilters })),
  })
);
