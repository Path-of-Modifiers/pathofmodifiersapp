import { createFileRoute } from "@tanstack/react-router";
import Header from "../../components/Common/Header";
import QueryButtons from "../../components/Common/QueryButtons";
import { Flex, Box, VStack } from "@chakra-ui/layout";
import { GraphInput } from "../../components/Input/GraphInput";
import GraphComponent from "../../components/Graph/GraphComponent";
import { useEffect, useRef, useState } from "react";
import { useGetGroupedModifiers } from "../../hooks/getData/prefetchGroupedModifiers";
import { useGetItemBaseTypes } from "../../hooks/getData/getBaseTypeCategories";
import { GroupedModifierByEffect, ItemBaseType } from "../../client";
import Footer from "../../components/Common/Footer";
import { ErrorMessage } from "../../components/Input/StandardLayoutInput/ErrorMessage";
import { useErrorStore } from "../../store/ErrorStore";

export const Route = createFileRoute("/_layout/")({
    component: Index,
});

// Index Component - This component is the main component for the index route.
function Index() {
    const [modifiers, setModifiers] = useState<GroupedModifierByEffect[]>([]);
    const [itemBaseTypes, setItemBaseTypes] = useState<ItemBaseType[]>([]);
    const [itemNames, setItemNames] = useState<string[]>([]);
    const requestGroupedModifiers = useGetGroupedModifiers();
    const requestItemBaseTypes = useGetItemBaseTypes();
    const { modifiersError, leagueError, resultError } = useErrorStore();
    const isFetched = useRef<boolean>(false);


    useEffect(() => {
        if (!isFetched.current) {
            const fetchData = async () => {
                const groupedModifiers = await requestGroupedModifiers
                const itemBaseTypes = await requestItemBaseTypes
                if (groupedModifiers) {
                    setModifiers(groupedModifiers.groupedModifiers);
                } if (itemBaseTypes) {
                    setItemBaseTypes(itemBaseTypes.itemBaseTypes);
                    setItemNames(itemBaseTypes.itemNames);
                }
                isFetched.current = true
            }
            fetchData()
        }
        }, [requestGroupedModifiers, requestItemBaseTypes]);


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
                        {modifiers.length > 0 && itemBaseTypes.length > 0 && (
                            <GraphInput
                                prefetchedmodifiers={modifiers}
                                prefetcheditembasetypes={itemBaseTypes}
                                prefecteditemnames={itemNames}
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

