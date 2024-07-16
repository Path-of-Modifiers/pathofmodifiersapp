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
  setItemSpecIdentified: (identified: boolean) => void;
  setItemName: (name: string) => void;
  setItemSpecMinIlvl: (minIlvl: number) => void;
  setItemSpecMaxIlvl: (maxIlvl: number) => void;
  setItemRarity: (rarity: string | undefined) => void;
  setItemSpecCorrupted: (corrupted: boolean) => void;
  setItemSpecDelve: (delve: boolean) => void;
  setItemSpecFractured: (fractured: boolean) => void;
  setItemSpecSynthesized: (synthesized: boolean) => void;
  setItemSpecElderInfluence: (elder: boolean) => void;
  setItemSpecShaperInfluence: (shaper: boolean) => void;
  setItemSpecCrusaderInfluence: (crusader: boolean) => void;
  setItemSpecRedeemerInfluence: (redeemer: boolean) => void;
  setItemSpecHunterInfluence: (hunter: boolean) => void;
  setItemSpecWarlordInfluence: (warlord: boolean) => void;
  setItemSpecReplica: (replica: boolean) => void;
  setItemSpecSearing: (searing: boolean) => void;
  setItemSpecTangled: (tangled: boolean) => void;
  setItemSpecIsRelic: (isRelic: boolean) => void;
  setItemSpecFoilVariation: (foilVariation: number) => void;
  setBaseType: (baseType: string | undefined) => void;
  setItemCategory: (category: string | undefined) => void;
  setItemSubCategory: (subCategory: string | undefined) => void;
  addModifierSpec: (modifierSpec: ModifierSpecState) => void;
  removeModifierSpec: (modifierId: number) => void;
  updateModifierSpec: (modifierSpec: ModifierSpecState) => void;
}

export interface ExpandedComponentState {
  expandedGraphInputFilters: boolean;
  setExpandedGraphInputFilters: (expandedGraphInputFilters: boolean) => void;
}
