import { create } from "zustand";
import { ErrorState } from "./StateInterface";

export const useErrorStore = create<ErrorState>((set) => ({
    leagueError: false,
    modifiersError: false,
    resultError: false,
    noRelatedUniqueError: false,
    itemDoesNotHaveSelectedModifiersError: false,
    setLeagueError: (leagueError: boolean) =>
        set((state) => ({ ...state, leagueError })),
    setModifiersError: (modifiersError: boolean) =>
        set((state) => ({ ...state, modifiersError })),
    setResultError: (resultError: boolean) =>
        set((state) => ({ ...state, resultError })),
    setNoRelatedUniqueError: (noRelatedUniqueError: boolean) =>
        set((state) => ({ ...state, noRelatedUniqueError })),
    setItemDoesNotHaveSelectedModifiersError: (
        itemDoesNotHaveSelectedModifiersError: boolean
    ) => set((state) => ({ ...state, itemDoesNotHaveSelectedModifiersError })),
}));
