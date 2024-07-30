import { create } from "zustand";
import { CaptchaState } from "./StateInterface";

export const useCaptchaStore = create<CaptchaState>((set) => ({
  status: "",
  setStatus: (status: string) => set((state) => ({ ...state, status })),
}));
