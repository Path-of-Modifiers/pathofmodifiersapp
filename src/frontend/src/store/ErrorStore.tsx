import { create } from "zustand";
import { ErrorState } from "./StateInterface";

export const useErrorStore = create<ErrorState>((set) => ({
  leagueError: false,
  noSelectedModifiersError: false,
  modifiersUnidentifiedError: false,
  currentlySelectedModifiersError: false,
  noRelatedUniqueError: false,
  baseSpecDoesNotMatchError: false,
  setLeagueError: (leagueError: boolean) =>
    set((state) => ({ ...state, leagueError })),
  setNoSelectedModifiersError: (noSelectedModifiersError: boolean) =>
    set((state) => ({ ...state, noSelectedModifiersError })),
  setModifiersUnidentifiedError: (modifiersUnidentifiedError: boolean) =>
    set((state) => ({ ...state, modifiersUnidentifiedError })),
  setCurrentlySelectedModifiersError: (currentlySelectedModifiersError: boolean) =>
    set((state) => ({ ...state, currentlySelectedModifiersError })),
  setNoRelatedUniqueError: (noRelatedUniqueError: boolean) =>
    set((state) => ({ ...state, noRelatedUniqueError })),
  setBaseSpecDoesNotMatchError: (baseSpecDoesNotMatchError: boolean) =>
    set((state) => ({ ...state, baseSpecDoesNotMatchError })),
}));
