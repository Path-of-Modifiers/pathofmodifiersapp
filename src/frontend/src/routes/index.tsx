import { MainPage } from "../components/Common/MainPage";
import { useGraphInputStore } from "../store/GraphInputStore";
import { useGetGroupedModifiers } from "../hooks/getData/prefetchGroupedModifiers";
import { useGetItemBaseTypes } from "../hooks/getData/getBaseTypeCategories";

import { useEffect, useRef } from "react";
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  beforeLoad: async () => {
    const searchParams = new URLSearchParams(location.hash.slice(1));
    const state = useGraphInputStore.getState();
    if (searchParams.size > 0) {
      state.getStoreFromHash(searchParams);
    } else {
      // This happens when being redirected from login
      state.setHashFromStore();
      state.setStateHash(undefined);
    }
  },
  component: Index,
});

// Index Component - This component is the main component for the index route.
function Index() {
  const {
    setChoosableModifiers,
    setChoosableItemBaseType,
    setChoosableItemNames,
    getStoreFromHash,
  } = useGraphInputStore();
  const requestGroupedModifiers = useGetGroupedModifiers();
  const requestItemBaseTypes = useGetItemBaseTypes();
  const isFetched = useRef<boolean>(false);

  useEffect(() => {
    if (!isFetched.current) {
      const fetchData = async () => {
        const groupedModifiers = await requestGroupedModifiers;
        const itemBaseTypes = await requestItemBaseTypes;
        if (groupedModifiers) {
          setChoosableModifiers(groupedModifiers.groupedModifiers);
        }
        if (itemBaseTypes) {
          setChoosableItemBaseType(itemBaseTypes.itemBaseTypes);
          setChoosableItemNames(itemBaseTypes.itemNames);
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
  ]);
  return <MainPage isReady={isFetched.current} />;
}