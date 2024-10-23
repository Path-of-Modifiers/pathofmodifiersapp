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

export interface WantedModifierSpecs extends WantedModifier {
  index: number;
  isSelected: boolean;
}

export interface PlotSettingsState {
  showChaos: boolean;
  showSecondary: boolean;
  setShowChaos: () => void;
  setShowSecondary: () => void;
}

export interface GraphInputState {
  clearClicked: boolean;
  queryClicked: boolean;
  league: string;
  itemName: string | undefined;
  itemSpec: ItemSpecState;
  baseSpec?: BaseSpecState;
  wantedModifiers: WantedModifier[];
  wantedModifierSpecs: WantedModifierSpecs[];
  plotQuery: PlotQuery;
  setQueryClicked: () => void;
  setPlotQuery: () => void;
  setClearClicked: () => void;
  setLeague: (league: string) => void;
  setItemSpecIdentified: (identified: boolean | undefined) => void;
  setItemName: (name: string | undefined) => void;
  setItemSpecMinIlvl: (minIlvl: number | undefined) => void;
  setItemSpecMaxIlvl: (maxIlvl: number | undefined) => void;
  setItemRarity: (rarity: string | undefined) => void;
  setItemSpecCorrupted: (corrupted: boolean | undefined) => void;
  setItemSpecDelve: (delve: boolean | undefined) => void;
  setItemSpecFractured: (fractured: boolean | undefined) => void;
  setItemSpecSynthesized: (synthesized: boolean | undefined) => void;
  setItemSpecElderInfluence: (elder: boolean | undefined) => void;
  setItemSpecShaperInfluence: (shaper: boolean | undefined) => void;
  setItemSpecCrusaderInfluence: (crusader: boolean | undefined) => void;
  setItemSpecRedeemerInfluence: (redeemer: boolean | undefined) => void;
  setItemSpecHunterInfluence: (hunter: boolean | undefined) => void;
  setItemSpecWarlordInfluence: (warlord: boolean | undefined) => void;
  setItemSpecReplica: (replica: boolean | undefined) => void;
  setItemSpecSearing: (searing: boolean | undefined) => void;
  setItemSpecTangled: (tangled: boolean | undefined) => void;
  setItemSpecIsRelic: (isRelic: boolean | undefined) => void;
  setItemSpecFoilVariation: (foilVariation: number | undefined) => void;
  setBaseType: (baseType: string | undefined) => void;
  setItemCategory: (category: string | undefined) => void;
  setItemSubCategory: (subCategory: string | undefined) => void;
  addModifierSpec: (wantedModifier: WantedModifier, index: number) => void;
  removeModifierSpec: (index_to_remove: number) => void;
  updateSelectedModifierSpec: (
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
