import { create } from "zustand";
import { TurnstileState } from "./StateInterface";
import { TurnstileResponse } from "../client";

export const useTurnstileStore = create<TurnstileState>((set) => ({
  turnstileResponse: undefined,
  setTurnstileResponse: (response: TurnstileResponse | undefined) =>
    set({ turnstileResponse: response }),
}));
