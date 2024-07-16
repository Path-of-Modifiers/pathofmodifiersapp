import { createLazyFileRoute } from "@tanstack/react-router";
import Header from "../components/Common/Header";
import QueryButtons from "../components/Common/QueryButtons";
import { Flex, Box, VStack } from "@chakra-ui/layout";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { GraphInput } from "../components/Input/GraphInput";
import GraphComponent from "../components/Graph/GraphComponent";
import img from "../assets/wallpap_castle_high_res.jpeg";
import { useEffect, useRef, useState } from "react";
import { prefetchedGroupedModifiers } from "../hooks/getData/prefetchGroupedModifiers";
import {
  BaseType,
  GroupedModifierByEffect,
  ItemBaseTypeCategory,
  ItemBaseTypeSubCategory,
} from "../client";
import { prefetchAllBaseTypeData } from "../hooks/getData/getBaseTypeCategories";

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
    <Flex direction="column" minHeight="100vh" bgImage={img} bgSize="cover">
      <Box mb={"7rem"}>
        <Header />
      </Box>

      <Flex
        direction="row"
        bg="ui.main"
        opacity={0.98}
        justifyContent="center"
        width={"bgBoxes.defaultBox"}
        p={2}
        borderRadius={10}
        borderTopColor={"ui.darkBrown"}
        borderTopWidth={1}
        alignSelf="center"
      >
        <QueryClientProvider client={queryClient}>
          <VStack width="100%">
            {modifiersData.length > 0 && baseTypes.length > 0 && (
              <GraphInput
                prefetchedmodifiers={modifiersData}
                prefetchbasetypes={baseTypes}
                prefetchcategories={categories}
                prefetchsubcategories={subCategories}
              />
            )}
            <QueryButtons />
            <GraphComponent
              width={"bgBoxes.mediumBox"}
              height={"bgBoxes.smallBox"}
            />
          </VStack>
        </QueryClientProvider>
      </Flex>
    </Flex>
  );
}
