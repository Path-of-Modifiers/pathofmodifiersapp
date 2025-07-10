import { create } from "zustand";
import { PlotSettingsState } from "./StateInterface";

export const usePlotSettingsStore = create<PlotSettingsState>((set) => ({
  showChaos: true,
  showSecondary: false,

  setShowChaos: (show: boolean) =>
    set(() => ({
      showChaos: show,
    })),
  setShowSecondary: (show: boolean) =>
    set(() => ({
      showSecondary: show,
    })),
}));
