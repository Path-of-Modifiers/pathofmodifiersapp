import { PlotQuery, TurnstileResponse } from "../client";

export interface InfluenceSpecState {
    elder?: boolean | null;
    shaper?: boolean | null;
    crusader?: boolean | null;
    redeemer?: boolean | null;
    hunter?: boolean | null;
    warlord?: boolean | null;
}

export interface ItemSpecState {
    name?: string | null;
    identified?: boolean | null;
    minIlvl?: number | null;
    maxIlvl?: number | null;
    rarity?: string | null;
    corrupted?: boolean | null;
    delve?: boolean | null;
    fractured?: boolean | null;
    synthesized?: boolean | null;
    replica?: boolean | null;
    influences?: InfluenceSpecState | null;
    searing?: boolean | null;
    tangled?: boolean | null;
    isRelic?: boolean | null;
    foilVariation?: number | null;
}

export interface BaseSpecState {
    baseType?: string | null;
    category?: string | null;
    subCategory?: string | null;
}

export interface ModifierLimitationState {
    minRoll?: number | null;
    maxRoll?: number | null;
    textRoll?: number | null;
}

export interface WantedModifier {
    modifierId: number;
    modifierLimitations?: ModifierLimitationState | null;
}
// Used to keep track of the different wanted modifiers for frontend
export interface WantedModifierExtended extends WantedModifier {
    index: number;
    isSelected: boolean;
}

export interface PlotSettingsState {
    showChaos: boolean;
    showSecondary: boolean;
    setShowChaos: () => void;
    setShowSecondary: () => void;
}
export type SetItemSpecMisc = (isItemSpecType: boolean | undefined) => void;

export interface GraphInputState {
    clearClicked: boolean;
    queryClicked: boolean;
    fetchStatus: string | undefined;
    league: string;
    itemName: string | undefined;
    itemSpec: ItemSpecState;
    baseSpec?: BaseSpecState;
    wantedModifiers: WantedModifier[];
    wantedModifierExtended: WantedModifierExtended[];
    plotQuery: PlotQuery;
    setQueryClicked: () => void;
    setFetchStatus: (fetchStatus: string | undefined) => void
    setPlotQuery: () => void;
    setClearClicked: () => void;
    setLeague: (league: string) => void;
    setItemName: (name: string | undefined) => void;
    setItemRarity: (rarity: string | undefined) => void;
    setItemSpecMinIlvl: (minIlvl: number | undefined) => void;
    setItemSpecMaxIlvl: (maxIlvl: number | undefined) => void;
    setItemSpecIdentified: SetItemSpecMisc;
    setItemSpecCorrupted: SetItemSpecMisc;
    setItemSpecDelve: SetItemSpecMisc;
    setItemSpecFractured: SetItemSpecMisc;
    setItemSpecSynthesized: SetItemSpecMisc;
    setItemSpecElderInfluence: SetItemSpecMisc;
    setItemSpecShaperInfluence: SetItemSpecMisc;
    setItemSpecCrusaderInfluence: SetItemSpecMisc;
    setItemSpecRedeemerInfluence: SetItemSpecMisc;
    setItemSpecHunterInfluence: SetItemSpecMisc;
    setItemSpecWarlordInfluence: SetItemSpecMisc;
    setItemSpecReplica: SetItemSpecMisc;
    setItemSpecSearing: SetItemSpecMisc;
    setItemSpecTangled: SetItemSpecMisc;
    setItemSpecIsRelic: SetItemSpecMisc;
    setItemSpecFoilVariation: (foilVariation: number | undefined) => void;
    setBaseType: (baseType: string | undefined) => void;
    setItemCategory: (category: string | undefined) => void;
    setItemSubCategory: (subCategory: string | undefined) => void;
    addWantedModifierExtended: (
        wantedModifier: WantedModifier,
        index: number
    ) => void;
    removeWantedModifierExtended: (index_to_remove: number) => void;
    updateSelectedWantedModifierExtended: (
        index_to_update: number,
        isSelected: boolean
    ) => void;
    setWantedModifierMinRoll: (
        modifierId: number,
        minRoll: number | undefined,
        index: number
    ) => void;
    setWantedModifierMaxRoll: (
        modifierId: number,
        maxRoll: number | undefined,
        index: number
    ) => void;
    setWantedModifierTextRoll: (
        modifierId: number,
        textRoll: number | undefined,
        index: number
    ) => void;
}

export interface ExpandedComponentState {
    expandedGraphInputFilters: boolean;
    expandedModifiers: boolean;
    expandedBaseType: boolean;
    expandedMiscItem: boolean;

    setExpandedGraphInputFilters: (expandedGraphInputFilters: boolean) => void;
    setExpandedModifiers: (expandedModifiers: boolean) => void;
    setExpandedBaseType: (expandedBaseType: boolean) => void;
    setExpandedMiscItem: (expandedMiscItem: boolean) => void;
}

export interface ErrorState {
    leagueError: boolean;
    modifiersError: boolean;
    resultError: boolean;
    setLeagueError: (leagueError: boolean) => void;
    setModifiersError: (modifiersError: boolean) => void;
    setResultError: (resultError: boolean) => void;
}

export interface TurnstileState {
    turnstileResponse: TurnstileResponse | undefined;
    setTurnstileResponse: (
        turnstileResponse: TurnstileResponse | undefined
    ) => void;
}
