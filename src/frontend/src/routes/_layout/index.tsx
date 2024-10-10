import { createFileRoute } from "@tanstack/react-router";
import Header from "../../components/Common/Header";
import QueryButtons from "../../components/Common/QueryButtons";
import { Flex, Box, VStack } from "@chakra-ui/layout";
import { QueryClient } from "@tanstack/react-query";
import { GraphInput } from "../../components/Input/GraphInput";
import GraphComponent from "../../components/Graph/GraphComponent";
import { useEffect, useRef, useState } from "react";
import { prefetchedGroupedModifiers } from "../../hooks/getData/prefetchGroupedModifiers";
import { GroupedModifierByEffect, ItemBaseType } from "../../client";
import { prefetchAllBaseTypeData } from "../../hooks/getData/getBaseTypeCategories";
import Footer from "../../components/Common/Footer";
import { ErrorMessage } from "../../components/Input/StandardLayoutInput/ErrorMessage";
import { useErrorStore } from "../../store/ErrorStore";

export const Route = createFileRoute("/_layout/")({
  component: Index,
});

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: Infinity,
    },
  },
});

// Index Component  -  This component is the main component for the index route.
function Index() {
  const [modifiersData, setModifiersData] = useState<GroupedModifierByEffect[]>(
    []
  );
  const [itemBaseTypes, setItemBaseTypes] = useState<ItemBaseType[]>([]);
  const [uniques, setUniques] = useState<string[]>([]);
  const { modifiersError, leagueError, resultError } = useErrorStore();
  const isFetched = useRef(false);

  useEffect(() => {
    if (!isFetched.current) {
      prefetchedGroupedModifiers(queryClient).then((data) => {
        setModifiersData(data.groupedModifiers);
      });
      prefetchAllBaseTypeData(queryClient).then((data) => {
        setItemBaseTypes(data.itemBaseTypes);
        setUniques(data.uniques);
      });
      isFetched.current = true; // Mark as fetched
    }
  }, []);

  return (
    <Flex
      direction="column"
      bg="ui.main"
      width="99vw"
      minWidth="bgBoxes.miniPBox"
    >
      <>
        <Box mb={"7rem"}>
          <Header />
        </Box>

        <Flex
          direction="row"
          bg="ui.secondary"
          justifyContent="center"
          maxWidth={"100%"}
          flexWrap="wrap"
          minHeight="100vh"
          p={3}
          pl={10}
          pr={10}
          borderTopRadius={10}
          borderTopColor={"ui.darkBrown"}
          borderTopWidth={1}
          alignSelf="center"
        >
          <VStack width={"bgBoxes.defaultBox"} height={"100%"} maxW={"100%"}>
            {modifiersData.length > 0 && itemBaseTypes.length > 0 && (
              <GraphInput
                prefetchedmodifiers={modifiersData}
                prefetcheditembasetypes={itemBaseTypes}
                prefetcheduniques={uniques}
              />
            )}
            <QueryButtons />
            {modifiersError && (
              <ErrorMessage
                alertTitle="No Modifiers Selected"
                alertDescription="Please select at least one modifier."
              />
            )}
            {leagueError && (
              <ErrorMessage
                alertTitle="No League Selected"
                alertDescription="Please select a league."
              />
            )}
            {resultError && (
              <ErrorMessage
                alertTitle="No Results Found"
                alertDescription="No results were found for the current query."
              />
            )}

            <GraphComponent
              width={"bgBoxes.mediumBox"}
              minH={"bgBoxes.smallBox"}
              height={"bgBoxes.smallBox"}
              maxW="98vw"
              mb="10rem"
              justifyItems={"center"}
            />
            <Footer />
          </VStack>
        </Flex>
      </>
    </Flex>
  );
}
