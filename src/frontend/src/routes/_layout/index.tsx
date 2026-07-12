import { useEffect, useRef } from "react";
import { createFileRoute } from "@tanstack/react-router";

import { MainPage } from "../../components/Common/MainPage";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { useGetGroupedModifiers } from "../../hooks/getData/prefetchGroupedModifiers";
import { useGetItemBaseTypes } from "../../hooks/getData/getBaseTypeCategories";
import { useGetLeagues } from "../../hooks/getData/getLeagues";
import { validateAndSetSearchParams } from "../../utils";
import { getCurrentLeague } from "../../hooks/graphing/utils";
import { useLeagueLaunchStats } from "../../store/LeagueLaunchStatsStore";
import { useQueryClient } from "@tanstack/react-query";

export const Route = createFileRoute("/_layout/")({
  beforeLoad: async () => {
    // const searchParams = new URLSearchParams(location.hash.slice(1));
    validateAndSetSearchParams();
  },
  component: Index,
});

// Index Component - This component is the main component for the index route.
function Index() {
  const {
    setChoosableModifiers,
    setChoosableItemBaseType,
    addLeague,
    setChoosableLeagues,
    setChoosableItemNames,
    getStoreFromHash,
    setHashFromStore,
  } = useGraphInputStore();
  const { setLeague, setLeagueLaunch } = useLeagueLaunchStats();
  const queryClient = useQueryClient();
  const requestGroupedModifiers = useGetGroupedModifiers();
  const requestItemBaseTypes = useGetItemBaseTypes(queryClient);
  const requestLeagues = useGetLeagues(queryClient);
  const isFetched = useRef<boolean>(false);

  useEffect(() => {
    if (!isFetched.current) {
      const fetchData = async () => {
        const groupedModifiers = await requestGroupedModifiers;
        const itemBaseTypes = await requestItemBaseTypes;
        const leagues = await requestLeagues;
        if (groupedModifiers) {
          setChoosableModifiers(groupedModifiers.groupedModifiers);
        }
        if (itemBaseTypes) {
          setChoosableItemBaseType(itemBaseTypes.itemBaseTypes);
          setChoosableItemNames(itemBaseTypes.itemNames);
        }
        if (leagues) {
          setChoosableLeagues(leagues.leagues);
          const currentLeague = getCurrentLeague(leagues.leagues);
          if (currentLeague !== undefined) {
            const leagueLaunch = new Date(currentLeague.validFrom);
            setLeagueLaunch(leagueLaunch);
            setLeague(currentLeague);
            addLeague(currentLeague.name);
            setHashFromStore();
          }
        }
        isFetched.current = true;
      };
      fetchData();
    }
  }, [
    requestGroupedModifiers,
    requestItemBaseTypes,
    setChoosableModifiers,
    setChoosableItemBaseType,
    setChoosableItemNames,
    getStoreFromHash,
    requestLeagues,
    setChoosableLeagues,
    setLeagueLaunch,
    setLeague,
  ]);
  return <MainPage isReady={isFetched.current} />;
}
