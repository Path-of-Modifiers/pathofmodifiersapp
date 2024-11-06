import { createFileRoute } from "@tanstack/react-router";
import Header from "../../components/Common/Header";
import QueryButtons from "../../components/Common/QueryButtons";
import { Flex, Box, VStack } from "@chakra-ui/layout";
import { GraphInput } from "../../components/Input/GraphInput";
import GraphComponent from "../../components/Graph/GraphComponent";
import { useEffect, useRef } from "react";
import { useGetGroupedModifiers } from "../../hooks/getData/prefetchGroupedModifiers";
import { useGetItemBaseTypes } from "../../hooks/getData/getBaseTypeCategories";
import Footer from "../../components/Common/Footer";
import { useGraphInputStore } from "../../store/GraphInputStore";

export const Route = createFileRoute("/_layout/")({
    component: Index,
});

// Index Component - This component is the main component for the index route.
function Index() {
    const {
        setChoosableModifiers,
        setChoosableItemBaseType,
        setChoosableItemNames,
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
    ]);

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
                    <VStack
                        width={"bgBoxes.defaultBox"}
                        height={"100%"}
                        maxW={"100%"}
                    >
                        <GraphInput />
                        <QueryButtons />

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
