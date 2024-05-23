import { create } from "zustand";
import {
  GraphInputState,
  ItemSpecState,
  ModifierSpecState,
} from "./StateInterface";
import { defaultLeague } from "../env-vars";

// Graph Input Store  -  This store is used to store graph input data.
export const useGraphInputStore = create<GraphInputState>((set) => ({
  clearClicked: false,
  league: defaultLeague,
  itemSpecState: {},
  baseSpec: {},
  modifierSpecs: [],

  setLeague: (league: string) => set(() => ({ league: league })),

  setClearClicked: () =>
    set(() => ({
      clearClicked: true,
      itemSpecState: {},
      modifierSpecs: [],
      baseSpec: {},
    })),

  setItemSpecIdentified: (identified: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, identified: identified },
    })),

  setItemName: (name: string) =>
    set((state) => ({ itemSpecState: { ...state.itemSpecState, name: name } })),

  setItemSpecElderInfluence: (elder: boolean) =>
    set((state) => ({
      itemSpecState: {
        ...state.itemSpecState,
        influences: {
          ...state.itemSpecState.influences,
          elder: elder,
        },
      },
    })),

  setItemSpecShaperInfluence: (shaper: boolean) =>
    set((state) => ({
      itemSpecState: {
        ...state.itemSpecState,
        influences: {
          ...state.itemSpecState.influences,
          shaper: shaper,
        },
      },
    })),

  setItemSpecCrusaderInfluence: (crusader: boolean) =>
    set((state) => ({
      itemSpecState: {
        ...state.itemSpecState,
        influences: {
          ...state.itemSpecState.influences,
          crusader: crusader,
        },
      },
    })),

  setItemSpecRedeemerInfluence: (redeemer: boolean) =>
    set((state) => ({
      itemSpecState: {
        ...state.itemSpecState,
        influences: {
          ...state.itemSpecState.influences,
          redeemer: redeemer,
        },
      },
    })),

  setItemSpecHunterInfluence: (hunter: boolean) =>
    set((state) => ({
      itemSpecState: {
        ...state.itemSpecState,
        influences: {
          ...state.itemSpecState.influences,
          hunter: hunter,
        },
      },
    })),

  setItemSpecWarlordInfluence: (warlord: boolean) =>
    set((state) => ({
      itemSpecState: {
        ...state.itemSpecState,
        influences: {
          ...state.itemSpecState.influences,
          warlord: warlord,
        },
      },
    })),

  setItemSpecReplica: (replica: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, replica: replica },
    })),

  setItemSpecSearingInfluence: (searing: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, searing: searing },
    })),

  setItemSpecTangledInfluence: (tangled: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, tangled: tangled },
    })),

  setItemSpecIsRelic: (isRelic: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, isRelic: isRelic },
    })),

  setItemSpecCorrupted: (corrupted: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, corrupted: corrupted },
    })),

  setItemSpecDelve: (delve: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, delve: delve },
    })),

  setItemSpecFractured: (fractured: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, fractured: fractured },
    })),

  setItemSpecSynthesized: (synthesized: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, synthesized: synthesized },
    })),

  setItemSpecSearing: (searing: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, searing: searing },
    })),

  setItemSpecTangled: (tangled: boolean) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, tangled: tangled },
    })),

  setItemSpecFoilVariation: (foilVariation: number) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, foilVariation: foilVariation },
    })),

  setItemSpecMinIlvl: (minIlvl: number) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, minIlvl: minIlvl },
    })),

  setItemSpecMaxIlvl: (maxIlvl: number) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, maxIlvl: maxIlvl },
    })),

  setItemRarity: (rarity: string | undefined) =>
    set((state) => ({
      itemSpecState: { ...state.itemSpecState, rarity: rarity },
    })),

  setItemSpec: (itemSpec: ItemSpecState) =>
    set(() => ({ itemSpecState: itemSpec })),

  setBaseType: (baseType: string | undefined) =>
    set((state) => ({
      baseSpec: { ...state.baseSpec, baseType: baseType },
    })),

  setItemCategory: (category: string | undefined) =>
    set((state) => ({
      baseSpec: { ...state.baseSpec, category: category },
    })),

  setItemSubCategory: (subCategory: string | undefined) =>
    set((state) => ({
      baseSpec: { ...state.baseSpec, subCategory: subCategory },
    })),

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
