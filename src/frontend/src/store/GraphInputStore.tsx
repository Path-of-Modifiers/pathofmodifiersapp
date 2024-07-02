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

  setItemSpecIdentified: (identified: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, identified: identified },
    })),

  setItemName: (name: string | undefined) =>
    set((state) => ({ itemSpec: { ...state.itemSpec, name: name } })),

  setItemSpecElderInfluence: (elder: boolean | undefined) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          elder: elder,
        },
      },
    })),

  setItemSpecShaperInfluence: (shaper: boolean | undefined) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          shaper: shaper,
        },
      },
    })),

  setItemSpecCrusaderInfluence: (crusader: boolean | undefined) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          crusader: crusader,
        },
      },
    })),

  setItemSpecRedeemerInfluence: (redeemer: boolean | undefined) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          redeemer: redeemer,
        },
      },
    })),

  setItemSpecHunterInfluence: (hunter: boolean | undefined) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          hunter: hunter,
        },
      },
    })),

  setItemSpecWarlordInfluence: (warlord: boolean | undefined) =>
    set((state) => ({
      itemSpec: {
        ...state.itemSpec,
        influences: {
          ...state.itemSpec.influences,
          warlord: warlord,
        },
      },
    })),

  setItemSpecReplica: (replica: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, replica: replica },
    })),

  setItemSpecSearingInfluence: (searing: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, searing: searing },
    })),

  setItemSpecTangledInfluence: (tangled: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, tangled: tangled },
    })),

  setItemSpecIsRelic: (isRelic: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, isRelic: isRelic },
    })),

  setItemSpecCorrupted: (corrupted: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, corrupted: corrupted },
    })),

  setItemSpecDelve: (delve: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, delve: delve },
    })),

  setItemSpecFractured: (fractured: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, fractured: fractured },
    })),

  setItemSpecSynthesized: (synthesized: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, synthesized: synthesized },
    })),

  setItemSpecSearing: (searing: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, searing: searing },
    })),

  setItemSpecTangled: (tangled: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, tangled: tangled },
    })),

  setItemSpecFoilVariation: (foilVariation: number | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, foilVariation: foilVariation },
    })),

  setItemSpecMinIlvl: (minIlvl: number | undefined) =>
    set((state) => {
      if (!minIlvl || minIlvl === 0) {
        minIlvl = undefined;
      }
      const itemSpec = { ...state.itemSpec, minIlvl: minIlvl };
      return { itemSpec: itemSpec };
    }),

  setItemSpecMaxIlvl: (maxIlvl: number | undefined) =>
    set((state) => {
      if (!maxIlvl || maxIlvl === 0) {
        maxIlvl = undefined;
      }
      const itemSpec = { ...state.itemSpec, maxIlvl: maxIlvl };
      return { itemSpec: itemSpec };
    }),

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

  addModifierSpec: (modifierSpec: ModifierSpecState, position?: number) =>
    set((state) => {
      if (position !== undefined) {
        return {
          modifierSpecs: [
            ...state.modifierSpecs.slice(0, position),
            modifierSpec,
            ...state.modifierSpecs.slice(position),
          ],
        };
      }
      return { modifierSpecs: [...state.modifierSpecs, modifierSpec] };
    }),

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

  setMinRollModifierSpec: (modifierId: number, minRoll: number | undefined) =>
    set((state) => {
      if (!minRoll || minRoll === 0) {
        minRoll = undefined;
      }
      const updatedSpecs = state.modifierSpecs.map((spec) =>
        spec.modifierId === modifierId
          ? {
              ...spec,
              modifierLimitations: {
                ...spec.modifierLimitations,
                minRoll: minRoll,
              },
            }
          : spec
      );
      return { modifierSpecs: updatedSpecs };
    }),

  setMaxRollModifierSpec: (modifierId: number, maxRoll: number | undefined) =>
    set((state) => {
      if (!maxRoll || maxRoll === 0) {
        maxRoll = undefined;
      }
      const updatedSpecs = state.modifierSpecs.map((spec) =>
        spec.modifierId === modifierId
          ? {
              ...spec,
              modifierLimitations: {
                ...spec.modifierLimitations,
                maxRoll: maxRoll,
              },
            }
          : spec
      );
      return { modifierSpecs: updatedSpecs };
    }),

  setTextRollModifierSpec: (modifierId: number, textRoll: number | undefined) =>
    set((state) => {
      const updatedSpecs = state.modifierSpecs.map((spec) =>
        spec.modifierId === modifierId
          ? {
              ...spec,
              modifierLimitations: {
                ...spec.modifierLimitations,
                textRoll: textRoll,
              },
            }
          : spec
      );
      return { modifierSpecs: updatedSpecs };
    }),
}));
