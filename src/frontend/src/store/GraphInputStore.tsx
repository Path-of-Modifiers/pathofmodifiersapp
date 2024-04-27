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
  itemRarity: "Unique",
  baseSpec: { baseType: "", category: "", subCategory: "" },
  modifierSpecs: [],

  setItemSpecState: (itemSpecState: ItemSpecState) =>
    set(() => ({ itemSpecState: itemSpecState })),
  setBaseSpec: (baseSpec: BaseSpecState) => set(() => ({ baseSpec: baseSpec })),
  setModifierSpecs: (modifierSpecs: ModifierSpecState[]) =>
    set(() => ({ modifierSpecs: modifierSpecs })),
}));
