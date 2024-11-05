import { create } from "zustand";
import {
    GraphInputState,
    ItemSpecState,
    WantedModifier,
    WantedModifierExtended,
} from "./StateInterface";

const defaultLeague = import.meta.env.VITE_APP_DEFAULT_LEAGUE;

// Graph Input Store  -  This store is used to store graph input data.
export const useGraphInputStore = create<GraphInputState>((set) => ({
    clearClicked: false,
    queryClicked: false,
    fetchStatus: undefined,
    league: defaultLeague,
    itemName: undefined,
    itemSpec: undefined,
    baseSpec: undefined,
    wantedModifiers: [],
    wantedModifierExtended: [],
    plotQuery: {
        league: defaultLeague,
        wantedModifiers: [],
    },

    setQueryClicked: () =>
        set(() => ({
            queryClicked: true,
        })),

    setFetchStatus: (fetchStatus: string | undefined) =>
        set(() => ({
            fetchStatus: fetchStatus,
        })),
    setPlotQuery: () =>
        set((state) => ({
            plotQuery: {
                league: state.league,
                itemSpecifications: state.itemSpec,
                baseSpec: state.baseSpec,
                wantedModifiers: state.wantedModifierExtended
                    .filter((wantedModifier) => wantedModifier.isSelected)
                    .map((wantedModifier) => ({
                        modifierId: wantedModifier.modifierId,
                        modifierLimitations: wantedModifier.modifierLimitations,
                    })),
            },
        })),

    setClearClicked: () =>
        set(() => ({
            clearClicked: true,
            itemName: undefined,
            itemSpec: {},
            wantedModifierExtended: [],
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
                    ...state.itemSpec?.influences,
                    elder: elder,
                },
            },
        })),

    setItemSpecShaperInfluence: (shaper: boolean | undefined) =>
        set((state) => ({
            itemSpec: {
                ...state.itemSpec,
                influences: {
                    ...state.itemSpec?.influences,
                    shaper: shaper,
                },
            },
        })),

    setItemSpecCrusaderInfluence: (crusader: boolean | undefined) =>
        set((state) => ({
            itemSpec: {
                ...state.itemSpec,
                influences: {
                    ...state.itemSpec?.influences,
                    crusader: crusader,
                },
            },
        })),

    setItemSpecRedeemerInfluence: (redeemer: boolean | undefined) =>
        set((state) => ({
            itemSpec: {
                ...state.itemSpec,
                influences: {
                    ...state.itemSpec?.influences,
                    redeemer: redeemer,
                },
            },
        })),

    setItemSpecHunterInfluence: (hunter: boolean | undefined) =>
        set((state) => ({
            itemSpec: {
                ...state.itemSpec,
                influences: {
                    ...state.itemSpec?.influences,
                    hunter: hunter,
                },
            },
        })),

    setItemSpecWarlordInfluence: (warlord: boolean | undefined) =>
        set((state) => ({
            itemSpec: {
                ...state.itemSpec,
                influences: {
                    ...state.itemSpec?.influences,
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
            const itemSpec = { ...state.itemSpec, minIlvl: minIlvl };
            return { itemSpec: itemSpec };
        }),

    setItemSpecMaxIlvl: (maxIlvl: number | undefined) =>
        set((state) => {
            const itemSpec = { ...state.itemSpec, maxIlvl: maxIlvl };
            return { itemSpec: itemSpec };
        }),

    setItemRarity: (rarity: string | undefined) =>
        set((state) => ({
            itemSpec: { ...state.itemSpec, rarity: rarity },
        })),

    setItemSpec: (itemSpec: ItemSpecState) =>
        set(() => ({ itemSpec: itemSpec })),

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

    addWantedModifierExtended: (
        wantedModifier: WantedModifier,
        index: number
    ) =>
        set((state) => {
            return {
                wantedModifierExtended: [
                    ...state.wantedModifierExtended,
                    { ...wantedModifier, index: index, isSelected: true },
                ],
            };
        }),

    updateSelectedWantedModifierExtended: (
        index_to_update: number,
        isSelected: boolean
    ) =>
        set((state) => {
            const chosenModifiersExtended = state.wantedModifierExtended.filter(
                (modifierExtended) => modifierExtended.index === index_to_update
            );
            return {
                wantedModifierExtended: [
                    ...state.wantedModifierExtended.filter(
                        (modifierExtended) =>
                            modifierExtended.index !== index_to_update
                    ),
                    ...chosenModifiersExtended.map(
                        (chosenModifierExtended) => ({
                            ...chosenModifierExtended,
                            isSelected: isSelected,
                        })
                    ),
                ],
            };
        }),

    removeWantedModifierExtended: (indexToRemove: number) =>
        set((state) => ({
            wantedModifierExtended: state.wantedModifierExtended.reduce(
                (prev, cur) =>
                    cur.index !== indexToRemove
                        ? [...prev, { ...cur, index: prev.length }]
                        : prev,
                [] as WantedModifierExtended[]
            ),
        })),

    setWantedModifierMinRoll: (
        modifierId: number,
        minRoll: number | undefined,
        index: number
    ) =>
        set((state) => {
            const updatedModifiersExtended = state.wantedModifierExtended.map(
                (wantedModifierExtended) => {
                    if (
                        wantedModifierExtended.modifierId === modifierId &&
                        wantedModifierExtended.index === index
                    ) {
                        if (minRoll === undefined) {
                            if (
                                !wantedModifierExtended.modifierLimitations
                                    ?.maxRoll
                            ) {
                                delete wantedModifierExtended[
                                    "modifierLimitations"
                                ];
                            } else {
                                delete wantedModifierExtended
                                    .modifierLimitations["minRoll"];
                            }
                            return wantedModifierExtended;
                        }
                        return {
                            ...wantedModifierExtended,
                            modifierLimitations: {
                                ...wantedModifierExtended.modifierLimitations,
                                minRoll: minRoll,
                            },
                        };
                    } else {
                        return wantedModifierExtended;
                    }
                }
            );
            return { wantedModifierExtended: updatedModifiersExtended };
        }),

    setWantedModifierMaxRoll: (
        modifierId: number,
        maxRoll: number | undefined,
        index: number
    ) =>
        set((state) => {
            const updatedModifiersExtended = state.wantedModifierExtended.map(
                (wantedModifierExtended) => {
                    if (
                        wantedModifierExtended.modifierId === modifierId &&
                        wantedModifierExtended.index === index
                    ) {
                        if (maxRoll === undefined) {
                            if (
                                !wantedModifierExtended.modifierLimitations
                                    ?.minRoll
                            ) {
                                delete wantedModifierExtended[
                                    "modifierLimitations"
                                ];
                            } else {
                                delete wantedModifierExtended
                                    .modifierLimitations["maxRoll"];
                            }
                            return wantedModifierExtended;
                        }
                        return {
                            ...wantedModifierExtended,
                            modifierLimitations: {
                                ...wantedModifierExtended.modifierLimitations,
                                maxRoll: maxRoll,
                            },
                        };
                    } else {
                        return wantedModifierExtended;
                    }
                }
            );
            return { wantedModifierExtended: updatedModifiersExtended };
        }),

    setWantedModifierTextRoll: (
        modifierId: number,
        textRoll: number | undefined,
        index: number
    ) =>
        set((state) => {
            const updatedModifiersExtended = state.wantedModifierExtended.map(
                (wantedModifierExtended) =>
                    wantedModifierExtended.modifierId === modifierId &&
                    wantedModifierExtended.index === index
                        ? {
                              ...wantedModifierExtended,
                              modifierLimitations:
                                  textRoll !== undefined
                                      ? {
                                            ...wantedModifierExtended.modifierLimitations,
                                            textRoll: textRoll,
                                        }
                                      : undefined,
                          }
                        : wantedModifierExtended
            );
            return { wantedModifierExtended: updatedModifiersExtended };
        }),
}));
