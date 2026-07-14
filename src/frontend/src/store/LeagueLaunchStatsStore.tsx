import { create } from "zustand";
import { LeagueLaunchStats } from "./StateInterface";
import { League } from "../client";

export const useLeagueLaunchStats = create<LeagueLaunchStats>((set) => ({
  league: {
    name: "Path of Exile",
    validFrom: "2013-10-23T21:00:00Z",
    leagueId: -1,
    version: 1.0,
  },
  leagueLaunch: new Date("2013-10-23T21:00:00Z"),
  hoursSinceLaunch: Number.NEGATIVE_INFINITY,
  setLeague: (league: League) => set(() => ({ league: league })),
  setLeagueLaunch: (leagueLaunch: Date) =>
    set(() => ({ leagueLaunch: leagueLaunch })),
  setHoursSinceLaunch: (hoursSinceLaunch: number) =>
    set(() => ({ hoursSinceLaunch: hoursSinceLaunch })),
}));
