import { create } from "zustand";
import { ErrorState } from "./StateInterface";

export const useErrorStore = create<ErrorState>((set) => ({
  leagueError: false,
  modifiersError: false,
  setLeagueError: (leagueError: boolean) =>
    set((state) => ({ ...state, leagueError })),
  setModifiersError: (modifiersError: boolean) =>
    set((state) => ({ ...state, modifiersError })),
}));
