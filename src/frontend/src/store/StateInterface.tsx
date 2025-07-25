import {
  GroupedModifierByEffect,
  ItemBaseType,
  PlotQuery,
  TurnstileResponse,
} from "../client";

export interface ChoosableModifiersExtended extends GroupedModifierByEffect {
  isNotChoosable?: boolean;
}
export interface ChoosableItemBaseTypesExtended extends ItemBaseType {
  isNotChoosable?: boolean;
}
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
  synthesised?: boolean | null;
  replica?: boolean | null;
  influences?: InfluenceSpecState | null;
  searing?: boolean | null;
  tangled?: boolean | null;
  foilVariation?: number | null;
}

export interface BaseSpecState {
  itemBaseTypeId?: number | null;
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
  relatedUniques?: string;
}

export interface PlotSettingsState {
  showChaos: boolean;
  showSecondary: boolean;
  setShowChaos: (show: boolean) => void;
  setShowSecondary: (show: boolean) => void;
}
export type SetItemSpecMisc = (isItemSpecType: boolean | undefined) => void;

export interface StateHash {
  leagues?: string[];
  itemName?: string;
  baseSpec?: string;
  itemSpec?: string;
  wantedModifierExtended?: string;
}

export interface GraphInputState {
  stateHash: StateHash | undefined;

  clearClicked: boolean;
  queryClicked: boolean;
  fetchStatus: string | undefined;

  choosableModifiers: ChoosableModifiersExtended[];
  choosableItemBaseType: ChoosableItemBaseTypesExtended[];
  choosableItemNames: string[];

  leagues: string[];

  itemName: string | undefined;
  itemSpec: ItemSpecState | undefined;
  baseSpec: BaseSpecState | undefined;

  wantedModifierExtended: WantedModifierExtended[];

  plotQuery: PlotQuery;

  getStoreFromHash: (searchParams: URLSearchParams) => void;
  setHashFromStore: () => void;
  setStateHash: (stateHash: StateHash | undefined) => void;

  setClearClicked: () => void;
  setQueryClicked: () => void;
  setFetchStatus: (fetchStatus: string | undefined) => void;

  setChoosableModifiers: (
    choosableModifiers: GroupedModifierByEffect[],
  ) => void;
  setChoosableItemBaseType: (choosableItemBaseType: ItemBaseType[]) => void;
  setChoosableItemNames: (choosableItemNames: string[]) => void;
  updateChoosable: (itemName: string | undefined) => void;

  setPlotQuery: (plotQuery: PlotQuery) => void;

  addLeague: (league: string) => void;
  removeLeague: (league: string) => void;
  removeAllLeagues: () => void;


  setItemName: (name: string | undefined) => void;

  setItemSpec: (itemSpec: ItemSpecState) => void;
  setItemRarity: (rarity: string | undefined) => void;
  setItemSpecMinIlvl: (minIlvl: number | undefined) => void;
  setItemSpecMaxIlvl: (maxIlvl: number | undefined) => void;
  setItemSpecIdentified: SetItemSpecMisc;
  setItemSpecCorrupted: SetItemSpecMisc;
  setItemSpecDelve: SetItemSpecMisc;
  setItemSpecFractured: SetItemSpecMisc;
  setItemSpecSynthesised: SetItemSpecMisc;
  setItemSpecElderInfluence: SetItemSpecMisc;
  setItemSpecShaperInfluence: SetItemSpecMisc;
  setItemSpecCrusaderInfluence: SetItemSpecMisc;
  setItemSpecRedeemerInfluence: SetItemSpecMisc;
  setItemSpecHunterInfluence: SetItemSpecMisc;
  setItemSpecWarlordInfluence: SetItemSpecMisc;
  setItemSpecReplica: SetItemSpecMisc;
  setItemSpecSearing: SetItemSpecMisc;
  setItemSpecTangled: SetItemSpecMisc;
  setItemSpecFoilVariation: (foilVariation: number | undefined) => void;

  setBaseSpec: (baseSpec: BaseSpecState) => void;
  setBaseType: (
    itemBaseTypeId: number | undefined,
    baseType: string | undefined,
  ) => void;
  setItemCategory: (category: string | undefined) => void;
  setItemSubCategory: (subCategory: string | undefined) => void;

  setWantedModifierExtended: (
    wantedModifierExtended: WantedModifierExtended[],
  ) => void;
  addWantedModifierExtended: (
    wantedModifier: WantedModifier,
    index: number,
    relatedUniques?: string,
  ) => void;
  removeWantedModifierExtended: (index_to_remove: number) => void;
  updateSelectedWantedModifierExtended: (
    index_to_update: number,
    isSelected: boolean,
  ) => void;
  setWantedModifierMinRoll: (
    modifierId: number,
    minRoll: number | undefined,
    index: number,
  ) => void;
  setWantedModifierMaxRoll: (
    modifierId: number,
    maxRoll: number | undefined,
    index: number,
  ) => void;
  setWantedModifierTextRoll: (
    modifierId: number,
    textRoll: number | undefined,
    index: number,
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
  noSelectedModifiersError: boolean;
  modifiersUnidentifiedError: boolean,
  currentlySelectedModifiersError: boolean,
  noRelatedUniqueError: boolean;
  baseSpecDoesNotMatchError: boolean;
  setLeagueError: (leagueError: boolean) => void;
  setNoSelectedModifiersError: (modifiersError: boolean) => void;
  setModifiersUnidentifiedError: (modifiersError: boolean) => void;
  setCurrentlySelectedModifiersError: (modifiersError: boolean) => void,
  setNoRelatedUniqueError: (noRelatedUniqueError: boolean) => void;
  setBaseSpecDoesNotMatchError: (baseSpecDoesNotMatchError: boolean) => void;
}

export interface TurnstileState {
  turnstileResponse: TurnstileResponse | undefined;
  setTurnstileResponse: (
    turnstileResponse: TurnstileResponse | undefined,
  ) => void;
}
