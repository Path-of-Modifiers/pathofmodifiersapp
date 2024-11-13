import { create } from "zustand";
import {
    BaseSpecState,
    ChoosableItemBaseTypesExtended,
    ChoosableModifiersExtended,
    GraphInputState,
    ItemSpecState,
    StateHash,
    WantedModifier,
    WantedModifierExtended,
} from "./StateInterface";
import { GroupedModifierByEffect, ItemBaseType, PlotQuery } from "../client";
import { encodeHash, decodeHash } from "./utils";

const defaultLeague = import.meta.env.VITE_APP_DEFAULT_LEAGUE;

// Graph Input Store  -  This store is used to store graph input data.
export const useGraphInputStore = create<GraphInputState>((set) => ({
    stateHash: undefined,

    clearClicked: false,
    queryClicked: false,
    fetchStatus: undefined,

    choosableModifiers: [],
    choosableItemBaseType: [],
    choosableItemNames: [],

    league: defaultLeague,

    itemName: undefined,
    itemSpec: undefined,
    baseSpec: undefined,

    wantedModifierExtended: [],

    plotQuery: {
        league: defaultLeague,
        wantedModifiers: [],
    },

    getStoreFromHash: (searchParams: URLSearchParams) =>
        set((state) => {
            const internalState: GraphInputState = { ...state };
            searchParams.forEach((value, key) => {
                if (key === "league") {
                    internalState.league = value;
                }
                if (key === "itemName") {
                    internalState.itemName = value;
                }
                if (key === "baseSpec") {
                    const baseSpec: BaseSpecState = JSON.parse(
                        decodeHash(value)
                    );
                    internalState.baseSpec = baseSpec;
                }
                if (key === "itemSpec") {
                    const itemSpec: ItemSpecState = JSON.parse(
                        decodeHash(value)
                    );
                    internalState.itemSpec = itemSpec;
                }
                if (key === "wantedModifierExtended") {
                    const wantedModifierExtended: WantedModifierExtended[] =
                        JSON.parse(decodeHash(value));
                    internalState.wantedModifierExtended =
                        wantedModifierExtended;
                }
            });
            return { ...internalState };
        }),
    setHashFromStore: () =>
        set((state) => {
            if (state.stateHash != null) return {};
            const searchParams = new URLSearchParams(location.hash.slice(1));
            const stateHash: StateHash = {};
            if (state.league != null) {
                stateHash.league = state.league;
                searchParams.set("league", state.league);
            }
            if (state.itemName != null) {
                stateHash.itemName = state.itemName;
                searchParams.set("itemName", state.itemName);
            }
            if (state.baseSpec != null) {
                const baseSpecHash = encodeHash(JSON.stringify(state.baseSpec));
                stateHash.baseSpec = baseSpecHash;
                searchParams.set("baseSpec", baseSpecHash);
            }
            if (state.itemSpec != null) {
                const itemSpecHash = encodeHash(JSON.stringify(state.itemSpec));
                stateHash.itemSpec = itemSpecHash;
                searchParams.set("itemSpec", itemSpecHash);
            }
            if (state.wantedModifierExtended.length > 0) {
                const wantedModifierExtendedHash = encodeHash(
                    JSON.stringify(state.wantedModifierExtended)
                );
                stateHash.wantedModifierExtended = wantedModifierExtendedHash;
                searchParams.set(
                    "wantedModifierExtended",
                    wantedModifierExtendedHash
                );
            }

            location.hash = searchParams.toString();
            return { stateHash: stateHash };
        }),

    setQueryClicked: () =>
        set(() => ({
            queryClicked: true,
        })),

    setFetchStatus: (fetchStatus: string | undefined) =>
        set(() => ({
            fetchStatus: fetchStatus,
        })),

    setChoosableModifiers: (choosableModifiers: GroupedModifierByEffect[]) =>
        set(() => ({
            choosableModifiers: choosableModifiers,
        })),

    setChoosableItemBaseType: (choosableItemBaseType: ItemBaseType[]) =>
        set(() => ({
            choosableItemBaseType: choosableItemBaseType,
        })),
    setChoosableItemNames: (choosableItemNames: string[]) =>
        set(() => ({
            choosableItemNames: choosableItemNames,
        })),

    updateChoosable: (itemName: string | undefined) =>
        set((state) => {
            let choosableModifiers: ChoosableModifiersExtended[];
            let choosableItemBaseType: ChoosableItemBaseTypesExtended[];
            if (itemName === undefined) {
                choosableModifiers = state.choosableModifiers.map(
                    (modifier) => ({
                        ...modifier,
                        isNotChoosable: false,
                    })
                );
                choosableItemBaseType = state.choosableItemBaseType.map(
                    (itemBaseType) => ({
                        ...itemBaseType,
                        isNotChoosable: false,
                    })
                );
            } else {
                choosableModifiers = state.choosableModifiers.map(
                    (modifier) => ({
                        ...modifier,
                        isNotChoosable:
                            !modifier.relatedUniques?.includes(itemName),
                    })
                );
                choosableItemBaseType = state.choosableItemBaseType.map(
                    (itemBaseType) => ({
                        ...itemBaseType,
                        isNotChoosable:
                            !itemBaseType.relatedUniques?.includes(itemName),
                    })
                );
            }
            return {
                choosableModifiers: choosableModifiers,
                choosableItemBaseType: choosableItemBaseType,
            };
        }),

    setPlotQuery: (plotQuery: PlotQuery) =>
        set(() => ({
            plotQuery: plotQuery,
        })),

    setClearClicked: () =>
        set(() => ({
            clearClicked: true,
            itemName: undefined,
            itemSpec: undefined,
            wantedModifierExtended: [],
            wantedModifiers: [],
            baseSpec: undefined,
        })),

    setLeague: (league: string) => set(() => ({ league: league })),

    setItemSpec: (itemSpec: ItemSpecState) =>
        set(() => ({ itemSpec: itemSpec })),

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

    setItemSpecSynthesised: (synthesised: boolean | undefined) =>
        set((state) => ({
            itemSpec: { ...state.itemSpec, synthesised: synthesised },
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

    setBaseSpec: (baseSpec: BaseSpecState) =>
        set(() => ({ baseSpec: baseSpec })),

    setBaseType: (
        itemBaseTypeId: number | undefined,
        baseType: string | undefined
    ) =>
        set((state) => ({
            baseSpec: {
                ...state.baseSpec,
                itemBaseTypeId: itemBaseTypeId,
                baseType: baseType,
            },
        })),

    setItemCategory: (category: string | undefined) =>
        set((state) => ({
            baseSpec: { ...state.baseSpec, category: category },
        })),

    setItemSubCategory: (subCategory: string | undefined) =>
        set((state) => ({
            baseSpec: { ...state.baseSpec, subCategory: subCategory },
        })),

    setWantedModifierExtended: (
        wantedModifierExtended: WantedModifierExtended[]
    ) => set(() => ({ wantedModifierExtended: wantedModifierExtended })),

    addWantedModifierExtended: (
        wantedModifier: WantedModifier,
        index: number,
        relatedUniques?: string
    ) =>
        set((state) => ({
            wantedModifierExtended: [
                ...state.wantedModifierExtended,
                {
                    ...wantedModifier,
                    index: index,
                    isSelected: true,
                    relatedUniques: relatedUniques,
                },
            ],
        })),

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
