import { create } from "zustand";
import {
  BaseSpecState,
  GraphInputState,
  ItemSpecState,
  ModifierSpecState,
} from "./StateInterface";

export const useGraphInputStore = create<GraphInputState>((set) => ({
  league: "",
  itemSpecState: {},
  baseSpec: { baseType: "", category: "", subCategory: "" },
  modifierSpecs: [],

  setLeague: (league: string) => set(() => ({ league: league })),

  setItemSpecState: (itemSpecState: ItemSpecState) =>
    set(() => ({ itemSpecState: itemSpecState })),
  setBaseSpec: (baseSpec: BaseSpecState) => set(() => ({ baseSpec: baseSpec })),

  addModifierSpec: (modifierSpec: ModifierSpecState) =>
    set((state) => ({ modifierSpecs: [...state.modifierSpecs, modifierSpec] })),

  removeModifierSpec: (modifierId: number) =>
    set((state) => ({
      modifierSpecs: state.modifierSpecs.filter(
        (modifierSpec) => modifierSpec.modifierId !== modifierId
      ),
    })),

  updateModifierSpec: (modifierSpec: ModifierSpecState) =>
    set((state) => ({
      modifierSpecs: state.modifierSpecs.map((spec) =>
        spec.modifierId === modifierSpec.modifierId ? modifierSpec : spec
      ),
    })),
}));
