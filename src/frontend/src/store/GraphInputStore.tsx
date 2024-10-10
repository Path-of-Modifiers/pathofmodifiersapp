import { create } from "zustand";
import {
  GraphInputState,
  ItemSpecState,
  WantedModifier,
} from "./StateInterface";

const defaultLeague = import.meta.env.VITE_APP_DEFAULT_LEAGUE;

// Graph Input Store  -  This store is used to store graph input data.
export const useGraphInputStore = create<GraphInputState>((set) => ({
  clearClicked: false,
  queryClicked: false,
  league: defaultLeague,
  itemName: undefined,
  itemSpec: {},
  baseSpec: {},
  wantedModifiers: [],
  nPossibleInputs: 1,
  wantedModifierSpecs: [],
  plotQuery: {
    league: defaultLeague,
    wantedModifiers: [],
  },

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
        wantedModifiers: state.wantedModifierSpecs.map((wantedModifier) => ({
          modifierId: wantedModifier.modifierId,
          modifierLimitations: wantedModifier.modifierLimitations,
        })),
      },
    })),

  setClearClicked: () =>
    set(() => ({
      clearClicked: true,
      itemSpec: {},
      wantedModifierSpecs: [],
      wantedModifiers: [],
      baseSpec: {},
    })),

  setLeague: (league: string) => set(() => ({ league: league })),

  setItemSpecIdentified: (identified: boolean | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, identified: identified },
    })),

  setItemName: (name: string | undefined) =>
    set((state) => ({
      itemSpec: { ...state.itemSpec, name: name },
      itemName: name,
    })),

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

  addModifierSpec: (
    wantedModifier: WantedModifier,
    index: number,
    nInputs: number
  ) =>
    set((state) => {
      state.setNPossibleInputs(nInputs);
      return {
        wantedModifierSpecs: [
          ...state.wantedModifierSpecs,
          { ...wantedModifier, index: index, nInputs: nInputs },
        ],
      };
    }),

  removeModifierSpec: (index_to_remove: number) =>
    set((state) => ({
      wantedModifierSpecs: state.wantedModifierSpecs.filter(
        (modifierSpec) => modifierSpec.index !== index_to_remove
      ),
    })),

  setWantedModifierMinRoll: (
    modifierId: number,
    minRoll: number | undefined,
    index: number
  ) =>
    set((state) => {
      const updatedSpecs = state.wantedModifierSpecs.map(
        (wantedModifierSpec) => {
          if (
            wantedModifierSpec.modifierId === modifierId &&
            wantedModifierSpec.index === index
          ) {
            if (minRoll === undefined) {
              delete wantedModifierSpec["modifierLimitations"];
              return wantedModifierSpec;
            }
            return {
              ...wantedModifierSpec,
              modifierLimitations: {
                ...wantedModifierSpec.modifierLimitations,
                minRoll: minRoll,
              },
            };
          } else {
            return wantedModifierSpec;
          }
        }
      );
      return { wantedModifierSpecs: updatedSpecs };
    }),

  setWantedModifierMaxRoll: (
    modifierId: number,
    maxRoll: number | undefined,
    index: number
  ) =>
    set((state) => {
      const updatedSpecs = state.wantedModifierSpecs.map(
        (wantedModifierSpec) =>
          wantedModifierSpec.modifierId === modifierId &&
          wantedModifierSpec.index === index
            ? {
                ...wantedModifierSpec,
                modifierLimitations:
                  maxRoll !== undefined
                    ? {
                        ...wantedModifierSpec.modifierLimitations,
                        maxRoll: maxRoll,
                      }
                    : undefined,
              }
            : wantedModifierSpec
      );
      return { wantedModifierSpecs: updatedSpecs };
    }),

  setWantedModifierTextRoll: (
    modifierId: number,
    textRoll: number | undefined,
    index: number
  ) =>
    set((state) => {
      console.log(modifierId, textRoll, index);
      const updatedSpecs = state.wantedModifierSpecs.map(
        (wantedModifierSpec) =>
          wantedModifierSpec.modifierId === modifierId &&
          wantedModifierSpec.index === index
            ? {
                ...wantedModifierSpec,
                modifierLimitations:
                  textRoll !== undefined
                    ? {
                        ...wantedModifierSpec.modifierLimitations,
                        textRoll: textRoll,
                      }
                    : undefined,
              }
            : wantedModifierSpec
      );
      return { wantedModifierSpecs: updatedSpecs };
    }),
  setNPossibleInputs: (n: number) =>
    set((state) => ({
      nPossibleInputs: state.nPossibleInputs < n ? n : state.nPossibleInputs,
    })),
  updateNPossibleInputs: () =>
    set((state) => {
      if (state.wantedModifierSpecs.length > 0) {
        const modifierSpecWMostInputs = state.wantedModifierSpecs.reduce(
          (prevVal, val) => (prevVal.nInputs > val.nInputs ? prevVal : val)
        );
        const maxNInputs = modifierSpecWMostInputs.nInputs;
        return { nPossibleInputs: maxNInputs };
      } else {
        return { nPossibleInputs: 1 };
      }
    }),
}));
