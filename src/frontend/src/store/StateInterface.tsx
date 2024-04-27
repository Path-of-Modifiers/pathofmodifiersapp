export interface InfluenceSpecState {
  elder: boolean;
  shaper: boolean;
  crusader: boolean;
  redeemer: boolean;
  hunter: boolean;
  warlord: boolean;
}

export interface ItemSpecState {
  name: string;
  identified: boolean;
  ilvl: number;
  rarity: string;
  corrupted: boolean;
  delve: boolean;
  fractured: boolean;
  synthesized: boolean;
  replica: boolean;
  influences: InfluenceSpecState;
  searing: boolean;
  tangled: boolean;
  isRelic: boolean;
  foilVariation: number;
}

export interface BaseSpecState {
  baseType: string;
  category: string;
  subCategory: string;
}

export interface ModifierLimitationState {
  minRoll: number;
  maxRoll: number;
  textRoll: number;
}

export interface ModifierSpecState {
  modifierId: string;
  position: number;
  limitations: ModifierLimitationState;
}

export interface GraphInputState {
  league: string;
  itemSpecState: ItemSpecState;
  baseSpec: BaseSpecState;
  modifierSpecs: ModifierSpecState[];
}
