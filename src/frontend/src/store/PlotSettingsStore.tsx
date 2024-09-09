import { create } from "zustand";
import { PlotSettingsState } from "./StateInterface";

export const usePlotSettingsStore = create<PlotSettingsState>((set) => ({
  showChaos: true,
  showSecondary: false,

  setShowChaos: () =>
    set((state) => ({
      showChaos: !state.showChaos,
    })),
  setShowSecondary: () =>
    set((state) => ({
      showSecondary: !state.showSecondary,
    })),
}));
