import {
  Box,
  Center,
  CloseButton,
  Flex,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";

import AddIconCheckbox from "../../Icon/AddIconCheckbox";

import { useEffect, useState } from "react";
import { GroupedModifierByEffect } from "../../../client";
import { useOutsideClick } from "../../../hooks/useOutsideClick";
import React from "react";
import { TextRollInput } from "./TextRollInput";
import { MinRollInput } from "./MinInput";
import { MaxRollInput } from "./MaxInput";
import { isArrayNullOrContainsOnlyNull } from "../../../hooks/utils";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { GetGroupedModifiersByEffect } from "../../../hooks/getGroupedModifiers";

export interface ModifierInput extends GroupedModifierByEffect {
  isSelected?: boolean;
  minRollInputs?: (number | null)[];
  maxRollInputs?: (number | null)[];
  textRollInputs?: (number | null)[];
}

export interface RenderInputProps {
  modifierSelected: ModifierInput;
  inputPosition: number;
  updateModifierInputFunction: UpdateModifierInputFunction;
}

export interface RenderInputMaxMinRollProps extends RenderInputProps {
  input: string | number | undefined | null;
}

export type UpdateModifierInputFunction = (
  modifierId: number,
  newMinRollInputs?: (number | null)[] | undefined,
  newMaxRollInputs?: (number | null)[] | undefined,
  newTextRollInputs?: (number | null)[] | undefined
) => void;

export const ModifierInput = () => {
  const [searchModifierText, setSearchModifierText] = useState("");

  const [filteredModifiers, setFilteredModifiers] = useState<ModifierInput[]>([
    {
      modifierId: [0],
      position: [0],
      effect: "",
      static: [false],
      minRoll: [0],
      maxRoll: [0],
      textRolls: [""],
    },
  ]);

  const [selectedModifiers, setSelectedModifiers] = useState<ModifierInput[]>(
    []
  );

  const { addModifierSpec, removeModifierSpec, updateModifierSpec } =
    useGraphInputStore();

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const [isExpanded, setIsExpanded] = useState(false);

  const modifiers: ModifierInput[] | undefined = GetGroupedModifiersByEffect();

  // Filter the modifiers based on the search text and selected modifiers.
  useEffect(() => {
    if (modifiers) {
      const filtered = modifiers
        .filter((modifier) =>
          modifier.effect
            .toLowerCase()
            .includes(searchModifierText.toLowerCase())
        )
        .filter(
          (modifier) =>
            !selectedModifiers.some(
              (selectedModifier) =>
                selectedModifier.modifierId[0] === modifier.modifierId[0]
            )
        );

      setFilteredModifiers(filtered);
    } else {
      setFilteredModifiers([
        {
          modifierId: [0],
          position: [0],
          effect: "",
          static: [false],
          minRoll: [0],
          maxRoll: [0],
          textRolls: [""],
        },
      ]);
    }

    const clearAllModifiers = () => {
      setSelectedModifiers([]);
      setSearchModifierText("");
    };

    if (clearClicked) {
      clearAllModifiers();
    }
  }, [searchModifierText, selectedModifiers, modifiers, clearClicked]);

  // Define the reference to the outside click hook. This is used to close the dropdown when clicking outside of it.
  const ref = useOutsideClick(() => {
    setIsExpanded(false);
    const graphstore = useGraphInputStore.getState();
    console.log(graphstore);
  });

  // Define the function to handle input changes
  const handleSearchModifierInputChange = (value: string) => {
    setSearchModifierText(value);
  };

  const handleModifierSelect = (selectedModifierEffect: ModifierInput) => {
    // Set the clicked modifier as selected
    selectedModifierEffect.isSelected = true;
    setSelectedModifiers((prevModifiers) => [
      ...prevModifiers,
      selectedModifierEffect,
    ]);

    // Initialize the input arrays for the selected modifier
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifierEffect.minRoll) &&
      selectedModifierEffect.minRoll
    ) {
      selectedModifierEffect.minRollInputs = new Array(
        selectedModifierEffect.minRoll.length
      ).fill(undefined);
    }
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifierEffect.maxRoll) &&
      selectedModifierEffect.maxRoll
    ) {
      selectedModifierEffect.maxRollInputs = new Array(
        selectedModifierEffect.maxRoll.length
      ).fill(undefined);
    }
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifierEffect.textRolls) &&
      selectedModifierEffect.textRolls
    ) {
      selectedModifierEffect.textRollInputs = new Array(
        selectedModifierEffect.textRolls.length
      ).fill(undefined);
    }

    // Add the selected modifier(s) to the global state store
    for (let i = 0; i < selectedModifierEffect.position.length; i++) {
      addModifierSpec({
        modifierId: selectedModifierEffect.modifierId[i],
        position: i,
        modifierLimitations: {
          minRoll: selectedModifierEffect.minRollInputs
            ? selectedModifierEffect.minRollInputs[i]
            : null,
          maxRoll: selectedModifierEffect.maxRollInputs
            ? selectedModifierEffect.maxRollInputs[i]
            : null,
          textRoll: selectedModifierEffect.textRollInputs
            ? selectedModifierEffect.textRollInputs[i]
            : null,
        },
      });
    }

    setSearchModifierText("");
    toggleExpand();
  };

  // Define the function to remove a selected modifier
  const handleRemoveModifier = (
    modifierId: number,
    modifierSelected: ModifierInput
  ) => {
    const effectToRemove = selectedModifiers.find(
      (modifier) => modifier.modifierId[0] === modifierId
    )?.effect;

    // Remove the selected modifier from the selectedModifiers list if it exists
    if (effectToRemove) {
      setSelectedModifiers((prevModifiers) =>
        prevModifiers.filter((modifier) => modifier.effect !== effectToRemove)
      );

      // Remove the modifier from the global state store
      for (let i = 0; i < modifierSelected.position.length; i++) {
        removeModifierSpec(modifierSelected.modifierId[i]);
      }
    }
  };

  // Define the function to handle checkbox changes for the selected modifiers
  const handleCheckboxChange = (
    modifierId: number,
    modifierSelected: ModifierInput,
    modifierIsSelected: boolean | undefined
  ) => {
    // Update the checkbox state of the selected modifier
    setSelectedModifiers((selectedModifiers) =>
      selectedModifiers.map((selectedModifier) =>
        selectedModifier.modifierId[0] === modifierId
          ? { ...selectedModifier, isSelected: !selectedModifier.isSelected }
          : selectedModifier
      )
    );

    // Add or remove the modifier from the global state store based on the checkbox state
    if (modifierIsSelected) {
      for (let i = 0; i < modifierSelected.position.length; i++) {
        removeModifierSpec(modifierSelected.modifierId[i]);
      }
    } else {
      for (let i = 0; i < modifierSelected.position.length; i++) {
        addModifierSpec({
          modifierId: modifierId,
          position: modifierSelected.position[i],
          modifierLimitations: {
            minRoll: modifierSelected.minRollInputs?.[i] ?? null,
            maxRoll: modifierSelected.maxRollInputs?.[i] ?? null,
            textRoll: modifierSelected.textRollInputs?.[i] ?? null,
          },
        });
      }
    }
  };

  // Define the function to toggle the expanded state of the dropdown
  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  // Define the function to handle scrolling in the dropdown
  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const bottom =
      e.currentTarget.scrollHeight - e.currentTarget.scrollTop ===
      e.currentTarget.clientHeight;
    if (bottom && !isExpanded) {
      setIsExpanded(true);
    }
  };

  // Define the function to update the modifier input
  const updateModifierInput = (
    modifierId: number,
    modifierToUpdate: ModifierInput,
    newMinRollInputs?: (number | null)[] | undefined,
    newMaxRollInputs?: (number | null)[] | undefined,
    newTextRollInputs?: (number | null)[] | undefined
  ): void => {
    // Update the modifier in the local state
    setSelectedModifiers((prevModifiers) => {
      const updatedModifiers = [...prevModifiers]; // Step 1: Create a copy of the array
      const index = updatedModifiers.findIndex(
        (modifier) => modifier.modifierId[0] === modifierId
      ); // Find index based on modifierId
      if (index !== -1) {
        // Ensure modifier with given modifierId exists
        const modifierToUpdate = { ...updatedModifiers[index] }; // Copy the modifier object
        if (newMinRollInputs) {
          modifierToUpdate.minRollInputs = newMinRollInputs.map(Number); // Update minRollInputs
        } else if (newMaxRollInputs) {
          modifierToUpdate.maxRollInputs = newMaxRollInputs.map(Number);
        } else if (newTextRollInputs) {
          modifierToUpdate.textRollInputs = newTextRollInputs;
        }
        updatedModifiers[index] = modifierToUpdate; // Replace the old modifier with the updated one
      }
      return updatedModifiers; // Set the updated array back to state
    });

    // Update the modifier in the global state store
    for (let i = 0; i < modifierToUpdate.position.length; i++) {
      updateModifierSpec({
        modifierId: modifierToUpdate.modifierId[i],
        position: modifierToUpdate.position[i],
        modifierLimitations: {
          minRoll: modifierToUpdate.minRollInputs?.[i] ?? null,
          maxRoll: modifierToUpdate.maxRollInputs?.[i] ?? null,
          textRoll: modifierToUpdate.textRollInputs?.[i] ?? null,
        },
      });
    }
  };

  // Render selected modifiers list
  const selectedModifiersList = selectedModifiers.map(
    (modifierSelected, index) => (
      <Flex key={index} bgColor={"ui.main"}>
        <Center width={9}>
          <AddIconCheckbox
            isChecked={modifierSelected.isSelected}
            key={modifierSelected.modifierId[0] + index}
            onChange={() => {
              if (modifierSelected.modifierId[0] !== null) {
                handleCheckboxChange(
                  modifierSelected.modifierId[0],
                  modifierSelected,
                  modifierSelected.isSelected
                );
              }
            }}
          />
        </Center>

        <Center bgColor={"ui.secondary"} width={"100%"}>
          <Text ml={3} mr={"auto"}>
            {modifierSelected.effect}
          </Text>

          <Flex justifyContent="flex-end">
            {/* Check if modifierSelected static exists and is all null */}
            {isArrayNullOrContainsOnlyNull(modifierSelected.static) &&
              (() => {
                const elements = [];
                for (
                  let modifierInputIndex = 0;
                  modifierInputIndex < modifierSelected.position.length;
                  modifierInputIndex++
                ) {
                  // Check if minRoll exists and are not all null. If so, create a MinRollInput component
                  if (
                    !isArrayNullOrContainsOnlyNull(modifierSelected.minRoll) &&
                    modifierSelected.minRoll &&
                    modifierSelected.minRoll[modifierInputIndex] !== null
                  ) {
                    const selectedModifierMinRollInput =
                      modifierSelected?.minRollInputs
                        ? modifierSelected.minRollInputs[modifierInputIndex]
                        : undefined;

                    elements.push(
                      <MinRollInput
                        modifierSelected={modifierSelected}
                        input={selectedModifierMinRollInput}
                        inputPosition={modifierInputIndex}
                        updateModifierInputFunction={() =>
                          updateModifierInput(
                            modifierSelected.modifierId[0],
                            modifierSelected,
                            modifierSelected.minRollInputs
                          )
                        }
                        key={"minRollPosition" + index + modifierInputIndex}
                      />
                    );
                  }

                  // Check if maxRoll exists and is not all null. If so, create a MaxRollInput component
                  if (
                    !isArrayNullOrContainsOnlyNull(modifierSelected.maxRoll) &&
                    modifierSelected.maxRoll &&
                    modifierSelected.maxRoll[modifierInputIndex] !== null
                  ) {
                    const selectedModifierMaxRollInput =
                      modifierSelected?.maxRollInputs
                        ? modifierSelected.maxRollInputs[modifierInputIndex]
                        : undefined;

                    elements.push(
                      <MaxRollInput
                        modifierSelected={modifierSelected}
                        input={selectedModifierMaxRollInput}
                        inputPosition={modifierInputIndex}
                        updateModifierInputFunction={() =>
                          updateModifierInput(
                            modifierSelected.modifierId[0],
                            modifierSelected,
                            undefined,
                            modifierSelected.maxRollInputs
                          )
                        }
                        key={"maxRollPosition" + index + modifierInputIndex}
                      />
                    );
                  }

                  // Check if textRolls exists and is not all null. If so, create a TextRollInput component
                  if (
                    !isArrayNullOrContainsOnlyNull(
                      modifierSelected.textRolls
                    ) &&
                    modifierSelected.textRolls &&
                    modifierSelected.textRolls[modifierInputIndex] !== null
                  ) {
                    elements.push(
                      <TextRollInput
                        modifierSelected={modifierSelected}
                        inputPosition={modifierInputIndex}
                        updateModifierInputFunction={() =>
                          updateModifierInput(
                            modifierSelected.modifierId[0],
                            modifierSelected,
                            undefined,
                            undefined,
                            modifierSelected.textRollInputs
                          )
                        }
                        key={"textRollPosition" + index + modifierInputIndex}
                      />
                    );
                  }
                }
                return elements;
              })()}
          </Flex>
        </Center>

        <Center>
          <CloseButton
            _hover={{ background: "gray.100", cursor: "pointer" }}
            onClick={() => {
              if (modifierSelected.modifierId[0] !== null) {
                handleRemoveModifier(
                  modifierSelected.modifierId[0],
                  modifierSelected
                );
              }
            }}
          />
        </Center>
      </Flex>
    )
  );

  // Render the list of modifiers in the dropdown
  const modifiersList = filteredModifiers.map((modifier) => (
    <Box
      key={modifier.modifierId[0]}
      p={2}
      _hover={{ background: "gray.100", cursor: "pointer" }}
      onClick={() => handleModifierSelect(modifier)}
    >
      {modifier.effect}
    </Box>
  ));

  return (
    <Flex direction="column" color="ui.dark" width={1200}>
      <Stack color={"ui.white"} mb={2}>
        {selectedModifiersList}
      </Stack>

      <Box bgColor={"ui.input"} color={"ui.white"} ref={ref} mr={8} ml={8}>
        <Input
          value={searchModifierText}
          onChange={(e) => handleSearchModifierInputChange(e.target.value)}
          placeholder="+ Add modifier"
          _placeholder={{ color: "ui.white" }}
          textAlign={"center"}
          focusBorderColor={"ui.white"}
          borderColor={"ui.grey"}
          onFocus={() => {
            if (!isExpanded) {
              toggleExpand();
            }
          }}
        />

        {isExpanded && (
          <Stack
            maxHeight={400}
            overflowY="auto"
            bgColor={"ui.input"}
            onScroll={handleScroll}
          >
            {modifiersList}
          </Stack>
        )}
      </Box>
    </Flex>
  );
};
