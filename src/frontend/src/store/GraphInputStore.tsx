import { create } from "zustand";
import {
  BaseSpecState,
  GraphInputState,
  ItemSpecState,
  ModifierSpecState,
} from "./StateInterface";

export const useGraphInputStore = create<GraphInputState>((set) => ({
  league: "Necropolis",
  itemSpecState: {
    name: "",
    identified: false,
    ilvl: 0,
    rarity: "",
    corrupted: false,
    delve: false,
    fractured: false,
    synthesized: false,
    replica: false,
    influences: {
      elder: false,
      shaper: false,
      crusader: false,
      redeemer: false,
      hunter: false,
      warlord: false,
    },
    searing: false,
    tangled: false,
    isRelic: false,
    foilVariation: 0,
  },
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
