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
  limitations?: ModifierLimitationState | null;
}

export interface GraphInputState {
  league: string;
  itemSpecState: ItemSpecState;
  baseSpec?: BaseSpecState;
  modifierSpecs: ModifierSpecState[];
  setLeague: (league: string) => void;
  setItemSpecIdentified: (identified: boolean) => void;
  setItemSpecMinIlvl: (minIlvl: number) => void;
  setItemSpecMaxIlvl: (maxIlvl: number) => void;
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
  setBaseSpec: (baseSpec: BaseSpecState) => void;
  addModifierSpec: (modifierSpec: ModifierSpecState) => void;
  removeModifierSpec: (modifierId: number) => void;
  updateModifierSpec: (modifierSpec: ModifierSpecState) => void;
}
