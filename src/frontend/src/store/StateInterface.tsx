import { PlotQuery } from "../client";

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

export interface ModifierSpecState {
  modifierId: number;
  position: number;
  modifierLimitations?: ModifierLimitationState | null;
}

export interface GraphInputState {
  clearClicked: boolean;
  queryClicked: boolean;
  league: string;
  itemSpec: ItemSpecState;
  baseSpec?: BaseSpecState;
  modifierSpecs: ModifierSpecState[];
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
  addModifierSpec: (modifierSpec: ModifierSpecState, position?: number) => void;
  removeModifierSpec: (modifierId: number) => void;
  updateModifierSpec: (modifierSpec: ModifierSpecState) => void;
  setMinRollModifierSpec: (
    modifierId: number,
    minRoll: number | undefined
  ) => void;
  setMaxRollModifierSpec: (
    modifierId: number,
    maxRoll: number | undefined
  ) => void;
  setTextRollModifierSpec: (
    modifierId: number,
    textRoll: number | undefined
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
