import { Box, CloseButton, Flex, Stack } from "@chakra-ui/react";
import { GroupedModifierProperties } from "../../../client";
import {
    SelectBoxInput,
    SelectBoxOptionValue,
    HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";
import { AddICheckText } from "../../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../../store/ExpandedComponentStore";
import { useEffect, useState } from "react";
import AddIconCheckbox from "../../Icon/AddIconCheckbox";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { FancySelectedModifier } from "./FancySelectedModifier";
import { ChoosableModifiersExtended } from "../../../store/StateInterface";
// For debugging purposes
// import { useOutsideClick } from "../../../hooks/useOutsideClick";

export interface ModifierOption extends SelectBoxOptionValue {
    isSelected?: boolean;
    index?: number;
    static?: boolean;
    relatedUniques?: string;
    groupedModifierProperties: GroupedModifierProperties;
}

export const ModifierInput = () => {
    const {
        wantedModifierExtended,
        choosableModifiers,
        addWantedModifierExtended,
        removeWantedModifierExtended,
        updateSelectedWantedModifierExtended,
    } = useGraphInputStore();

    const mapChoosableModifiersExtendedtoModifierOption = (
        choosableModifiersExtended: ChoosableModifiersExtended[]
    ) =>
        choosableModifiersExtended.map((prefetchedModifier) => ({
            value: prefetchedModifier.effect,
            label: prefetchedModifier.effect,
            regex: prefetchedModifier.regex,
            static: prefetchedModifier.static ?? undefined,
            relatedUniques: prefetchedModifier.relatedUniques ?? undefined,
            groupedModifierProperties:
                prefetchedModifier.groupedModifierProperties,
        }));
    const [choosableModifierOptions, setChoosableModifierOptions] = useState<
        ModifierOption[]
    >(mapChoosableModifiersExtendedtoModifierOption(choosableModifiers));

    useEffect(() => {
        setChoosableModifierOptions(
            mapChoosableModifiersExtendedtoModifierOption(
                choosableModifiers.filter(
                    (modifier) => !modifier.isNotChoosable
                )
            )
        );
    }, [choosableModifiers]);

    let prevSelectedModifiers: ModifierOption[] = [];
    if (wantedModifierExtended.length > 0) {
        prevSelectedModifiers = wantedModifierExtended.reduce(
            (selectedModifiers, wantedModifier) => {
                const prevSelectedModifier = choosableModifierOptions.find(
                    (modifier) =>
                        modifier.groupedModifierProperties.modifierId.includes(
                            wantedModifier.modifierId
                        )
                );
                if (prevSelectedModifier === undefined) {
                    return selectedModifiers;
                }

                return [
                    ...selectedModifiers,
                    {
                        ...prevSelectedModifier,
                        isSelected: wantedModifier.isSelected,
                        index: wantedModifier.index,
                    },
                ];
            },
            [] as ModifierOption[]
        );
    }

    const [selectedModifiers, setSelectedModifiers] = useState<
        ModifierOption[]
    >(prevSelectedModifiers);

    // For debugging purposes
    // const ref = useOutsideClick(() => {
    //     const store = useGraphInputStore.getState();
    //     console.log("STORE", store);
    //     // console.log("query ->", store.wantedModifierExtended);
    // });

    // NOTE: The index, which is the selected modifier's position in
    //`selectedModifiers` is used as a unique identifier both internally
    // in `ModifierInput` but also for `WantedModifiersExtended` which allows
    // multiple of the same modifier to be present in `WantedModifier`
    // by extension.
    const handleModifierSelect: HandleChangeEventFunction = (
        newValue,
        overrideIndex?: number
    ) => {
        const newlySelectedModifier = choosableModifierOptions.find(
            (modifier) => modifier.label === newValue?.label
        );
        if (!newlySelectedModifier) {
            return;
        }

        newlySelectedModifier.isSelected = true;
        // Note: currently not in use, but may be useful going forward
        // Removes the current modifier and replaces it with the new
        if (overrideIndex !== undefined) {
            newlySelectedModifier.index = overrideIndex;
            setSelectedModifiers((currentSelectedModifiers) => [
                ...currentSelectedModifiers.slice(0, overrideIndex),
                newlySelectedModifier,
                ...currentSelectedModifiers.slice(overrideIndex + 1),
            ]);

            removeWantedModifierExtended(overrideIndex);
            newlySelectedModifier.groupedModifierProperties.modifierId.map(
                (modifierId) => {
                    addWantedModifierExtended(
                        { modifierId: modifierId },
                        overrideIndex,
                        newlySelectedModifier.relatedUniques
                    );
                }
            );
        } else {
            setSelectedModifiers((currentSelectedModifiers) => [
                ...currentSelectedModifiers,
                { ...newlySelectedModifier, index: selectedModifiers.length },
            ]);
            newlySelectedModifier.groupedModifierProperties.modifierId.map(
                (modifierId) => {
                    addWantedModifierExtended(
                        { modifierId: modifierId },
                        selectedModifiers.length,
                        newlySelectedModifier.relatedUniques
                    );
                }
            );
        }
    };

    const { setExpandedModifiers } = useExpandedComponentStore();
    const expandedModifiers = useExpandedComponentStore(
        (state) => state.expandedModifiers
    );
    const handleExpanded = () => {
        setExpandedModifiers(!expandedModifiers);
    };

    const handleCheckboxChange = (
        selectedModifier: ModifierOption,
        index_to_handle: number
    ) => {
        selectedModifier.isSelected = !selectedModifier.isSelected;
        updateSelectedWantedModifierExtended(
            index_to_handle,
            selectedModifier.isSelected
        );
    };

    // Removes the modifier
    const handleRemoveModifier = (indexToRemove: number) => {
        const modifierToRemove = selectedModifiers.find(
            (modifier) => modifier.index === indexToRemove
        );
        if (modifierToRemove) {
            setSelectedModifiers((currentSelectedModifiers) =>
                currentSelectedModifiers.reduce(
                    (prev, cur) =>
                        cur.index !== indexToRemove
                            ? [...prev, { ...cur, index: prev.length }]
                            : prev,
                    [] as ModifierOption[]
                )
            );
            removeWantedModifierExtended(indexToRemove);
        }
    };

    const { clearClicked } = useGraphInputStore();

    // removes all selected modifiers
    useEffect(() => {
        if (clearClicked) {
            setSelectedModifiers([]);
        }
    }, [clearClicked]);

    const selectedModifierSelectBoxes = selectedModifiers.map(
        (selectedModifier, selectedIndex) => (
            <Flex
                key={selectedIndex}
                bgColor={"ui.secondary"}
                flexDirection={"row"}
                maxWidth="95vw"
                alignItems={"center"}
                gap={2}
            >
                <AddIconCheckbox
                    isChecked={selectedModifier.isSelected}
                    key={selectedIndex}
                    onChange={() => {
                        if (
                            selectedModifier.groupedModifierProperties
                                .modifierId[0] !== null
                        ) {
                            handleCheckboxChange(
                                selectedModifier,
                                selectedIndex
                            );
                        }
                    }}
                />
                <FancySelectedModifier
                    selectedModifier={selectedModifier}
                    index={selectedIndex}
                    isDimmed={!selectedModifier.isSelected}
                />
                <CloseButton
                    _hover={{ background: "gray.100", cursor: "pointer" }}
                    onClick={() => {
                        handleRemoveModifier(selectedIndex);
                    }}
                />
            </Flex>
        )
    );

    return (
        <Flex direction="column" color="ui.dark" width={"inputSizes.ultraBox"}>
            <Box mb={2}>
                <AddICheckText
                    text="Modifiers"
                    isChecked={expandedModifiers}
                    onChange={handleExpanded}
                />
            </Box>
            {expandedModifiers && (
                <Box>
                    <Stack color={"ui.white"} width="100%" mb={2}>
                        {selectedModifierSelectBoxes}
                    </Stack>

                    {/* mx here needs to be same length as checkboxes in selectedModifiersList */}
                    <Flex
                        bgColor={"ui.secondary"}
                        flexDirection={"row"}
                        maxWidth="95vw"
                        alignItems={"center"}
                        gap={2}
                        // ref={ref}
                    >
                        <AddIconCheckbox dontshow />
                        <SelectBoxInput
                            handleChange={handleModifierSelect}
                            optionsList={choosableModifierOptions}
                            defaultText="+ Add Modifier"
                            multipleValues={true}
                            id={`modifierInput-${selectedModifiers.length}`}
                            flexProps={{
                                width: "100%",
                                textAlign: "center",
                                _focusWithin: { textAlign: "left" },
                            }}
                        />
                        <Box boxSize="28px" minW="28px" />
                    </Flex>
                </Box>
            )}
        </Flex>
    );
};
