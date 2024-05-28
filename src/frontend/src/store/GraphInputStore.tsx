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
  queryClicked: false,
  league: defaultLeague,
  itemSpec: {},
  baseSpec: {},
  modifierSpecs: [],
  plotQuery: { league: "", itemSpecifications: {}, wantedModifiers: [] },

  setQueryClicked: () =>
    set(() => ({
      queryClicked: true,
    })),

  setPlotQuery: () =>
    set((state) => ({
      plotQuery: {
        league: state.league,
        itemSpecifications: state.itemSpec,
        baseSpec: state.baseSpec,
        wantedModifiers: state.modifierSpecs,
      },
    })),

  setLeague: (league: string) => set(() => ({ league: league })),

  setClearClicked: () =>
    set(() => ({
      clearClicked: true,
      itemSpec: {},
      modifierSpecs: [],
      baseSpec: {},
    })),

  setItemSpecIdentified: (identified: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, identified: identified },
    })),

  setItemName: (name: string) =>
    set((state) => ({ itemSpec: { ...state.itemSpec, name: name } })),

  setItemSpecElderInfluence: (elder: boolean) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          elder: elder,
        },
      },
    })),

  setItemSpecShaperInfluence: (shaper: boolean) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          shaper: shaper,
        },
      },
    })),

  setItemSpecCrusaderInfluence: (crusader: boolean) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          crusader: crusader,
        },
      },
    })),

  setItemSpecRedeemerInfluence: (redeemer: boolean) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          redeemer: redeemer,
        },
      },
    })),

  setItemSpecHunterInfluence: (hunter: boolean) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          hunter: hunter,
        },
      },
    })),

  setItemSpecWarlordInfluence: (warlord: boolean) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          warlord: warlord,
        },
      },
    })),

  setItemSpecReplica: (replica: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, replica: replica },
    })),

  setItemSpecSearingInfluence: (searing: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, searing: searing },
    })),

  setItemSpecTangledInfluence: (tangled: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, tangled: tangled },
    })),

  setItemSpecIsRelic: (isRelic: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, isRelic: isRelic },
    })),

  setItemSpecCorrupted: (corrupted: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, corrupted: corrupted },
    })),

  setItemSpecDelve: (delve: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, delve: delve },
    })),

  setItemSpecFractured: (fractured: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, fractured: fractured },
    })),

  setItemSpecSynthesized: (synthesized: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, synthesized: synthesized },
    })),

  setItemSpecSearing: (searing: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, searing: searing },
    })),

  setItemSpecTangled: (tangled: boolean) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, tangled: tangled },
    })),

  setItemSpecFoilVariation: (foilVariation: number) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, foilVariation: foilVariation },
    })),

  setItemSpecMinIlvl: (minIlvl: number) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, minIlvl: minIlvl },
    })),

  setItemSpecMaxIlvl: (maxIlvl: number) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, maxIlvl: maxIlvl },
    })),

  setItemRarity: (rarity: string | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, rarity: rarity },
    })),

  setItemSpec: (itemSpec: ItemSpecState) => set(() => ({ itemSpec: itemSpec })),

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
