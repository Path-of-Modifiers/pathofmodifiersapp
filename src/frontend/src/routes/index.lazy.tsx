import { createLazyFileRoute } from "@tanstack/react-router";
import Cookies from "js-cookie";
import Header from "../components/Common/Header";
import QueryButtons from "../components/Common/QueryButtons";
import { Flex, Box, VStack, Center } from "@chakra-ui/layout";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GraphInput } from "../components/Input/GraphInput";
import GraphComponent from "../components/Graph/GraphComponent";
import { useEffect, useRef, useState } from "react";
import { prefetchedGroupedModifiers } from "../hooks/getData/prefetchGroupedModifiers";
import {
  BaseType,
  GroupedModifierByEffect,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../client";
import { prefetchAllBaseTypeData } from "../hooks/getData/getBaseTypeCategories";
import Footer from "../components/Common/Footer";
import { ErrorMessage } from "../components/Input/StandardLayoutInput/ErrorMessage";
import { useErrorStore } from "../store/ErrorStore";
import CaptchaPage from "../components/Page/CaptchaPage";

export const Route = createLazyFileRoute("/")({
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
  const [baseTypes, setBaseTypes] = useState<BaseType[]>([]);
  const [categories, setCategories] = useState<ItemBaseTypeCategory[]>([]);
  const [subCategories, setSubCategories] = useState<ItemBaseTypeSubCategory[]>(
    []
  );
  const { modifiersError, leagueError, resultError } = useErrorStore();
  const status = Cookies.get("cf-captcha-status");
  const isFetched = useRef(false);

  useEffect(() => {
    if (!isFetched.current) {
      prefetchedGroupedModifiers(queryClient).then((data) => {
        setModifiersData(data.groupedModifiers);
      });
      prefetchAllBaseTypeData(queryClient).then((data) => {
        setBaseTypes(data.baseTypes);
        setCategories(data.itemBaseTypeCategory);
        setSubCategories(data.itemBaseTypeSubCategory);
      });
      isFetched.current = true; // Mark as fetched
    }
  }, []);
  return (
    <>
      <Flex
        direction="column"
        minHeight="100rem"
        bg="ui.main"
        width="99vw"
        minWidth="bgBoxes.miniPBox"
      >
        <Center mt={"7rem"}>
          <CaptchaPage />
        </Center>
        {status === "solved" && (
          <>
            <Box mb={"7rem"}>
              <Header />
            </Box>

            <Flex
              direction="row"
              bg="ui.secondary"
              justifyContent="center"
              maxWidth={"100%"}
              width="bgBoxes.defaultBox"
              flexWrap="wrap"
              minHeight="100rem"
              p={2}
              borderTopRadius={10}
              borderTopColor={"ui.darkBrown"}
              borderTopWidth={1}
              alignSelf="center"
            >
              <QueryClientProvider client={queryClient}>
                <VStack>
                  {modifiersData.length > 0 && baseTypes.length > 0 && (
                    <GraphInput
                      prefetchedmodifiers={modifiersData}
                      prefetchbasetypes={baseTypes}
                      prefetchcategories={categories}
                      prefetchsubcategories={subCategories}
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
                    height={"bgBoxes.smallBox"}
                    maxW="98vw"
                    maxH="98vh"
                  />
                  <Footer />
                </VStack>
              </QueryClientProvider>
            </Flex>
          </>
        )}
      </Flex>
    </>
  );
}
