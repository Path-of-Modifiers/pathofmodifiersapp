import {
  Box,
  Center,
  CloseButton,
  Flex,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";

import AddIconCheckbox from "../Icon/AddIconCheckbox";

import { useEffect, useState } from "react";
import { GroupedModifierByEffect } from "../../client";
import { useOutsideClick } from "../../hooks/useOutsideClick";
import React from "react";
import { modifiers } from "../../test_data/modifier_data";
import { TextRollInput } from "../Input/TextRollInput";
import { MinRollInput } from "../Input/MinRollInput";
import { MaxRollInput } from "../Input/MaxRollInput";
// import { GetGroupedModifiersByEffect } from "../../hooks/getGroupedModifiers";

export const ModifierInput = () => {
  return <ModifierListInput />;
};

export interface ModifierInput extends GroupedModifierByEffect {
  isSelected?: boolean;
  minRollInputs?: (number | null)[];
  maxRollInputs?: (number | null)[];
  textRollInputs?: (string | null)[];
}

export interface RenderInputProps {
  modifierSelected: ModifierInput;
  inputPosition: number;
  updateModifierInputFunction: UpdateModifierInputFunction;
}

export interface RenderInputMaxMinRollProps extends RenderInputProps {
  input: string | number | undefined | null;
  inputPosition: number;
}

export type UpdateModifierInputFunction = (
  modifierId: number,
  newMinRollInputs?: (number | null)[] | undefined,
  newMaxRollInputs?: (number | null)[] | undefined,
  newTextRollInputs?: (string | null)[] | undefined
) => void;

const ModifierListInput = () => {
  const [searchModifierText, setSearchModifierText] = useState("");

  const [filteredModifiers, setFilteredModifiers] = useState<ModifierInput[]>([
    {
      modifierId: [0],
      position: [0],
      effect: "",
    },
  ]);

  const [selectedModifiers, setSelectedModifiers] = useState<ModifierInput[]>(
    []
  );

  const [isExpanded, setIsExpanded] = useState(false);

  // const modifiers: ModifierInput[] | undefined = GetGroupedModifiersByEffect();

  useEffect(() => {
    const testModifiers: ModifierInput[] = modifiers;

    if (testModifiers) {
      const filtered = testModifiers
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
    }
  }, [searchModifierText, selectedModifiers]);

  const ref = useOutsideClick(() => {
    setIsExpanded(false);
    console.log("Selected modifiers: \n");
    console.log(selectedModifiers);
    console.log("Filtered modifiers: \n");
    console.log(filteredModifiers);
  });

  // Define the function to handle input changes
  const handleInputChange = (value: string) => {
    // Regular expression to allow numbers and scientific notation
    // const scientificPattern = /^-?\d*\.?\d*(e-?\d+)?$/i;
    setSearchModifierText(value);
  };

  const handleModifierSelect = (selectedModifierEffect: ModifierInput) => {
    // Set the clicked modifier as selected
    selectedModifierEffect.isSelected = true;
    setSelectedModifiers((prevModifiers) => [
      ...prevModifiers,
      selectedModifierEffect,
    ]);

    if (
      !isArrayNullOrContainsOnlyNull(selectedModifierEffect.minRoll) &&
      selectedModifierEffect.minRoll
    ) {
      selectedModifierEffect.minRollInputs = new Array(
        selectedModifierEffect.minRoll.length
      ).fill(undefined);

      if (selectedModifierEffect.minRollInputs !== undefined) {
        for (let i = 0; i < selectedModifierEffect.minRoll.length; i++) {
          selectedModifierEffect.minRollInputs[i] =
            selectedModifierEffect.minRoll[i];
        }
      }
    }
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifierEffect.maxRoll) &&
      selectedModifierEffect.maxRoll
    ) {
      selectedModifierEffect.maxRollInputs = new Array(
        selectedModifierEffect.maxRoll.length
      ).fill(undefined);

      if (selectedModifierEffect.maxRollInputs !== undefined) {
        for (let i = 0; i < selectedModifierEffect.maxRoll.length; i++) {
          selectedModifierEffect.maxRollInputs[i] =
            selectedModifierEffect.maxRoll[i];
        }
      }
    }
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifierEffect.textRolls) &&
      selectedModifierEffect.textRolls
    ) {
      selectedModifierEffect.textRollInputs = new Array(
        selectedModifierEffect.textRolls.length
      ).fill(undefined);

      if (selectedModifierEffect.textRollInputs !== undefined) {
        for (let i = 0; i < selectedModifierEffect.textRolls.length; i++) {
          if (
            selectedModifierEffect.textRolls[i] !== null &&
            selectedModifierEffect.textRolls[i] !== undefined
          ) {
            selectedModifierEffect.textRollInputs[i] =
              selectedModifierEffect.textRolls[i]?.split("-")[0] as string;
            break;
          }
        }
      }
    }

    setSearchModifierText("");
    toggleExpand();
  };

  const handleRemoveModifier = (id: number) => {
    const effectToRemove = selectedModifiers.find(
      (modifier) => modifier.modifierId[0] === id
    )?.effect;

    if (effectToRemove) {
      setSelectedModifiers((prevModifiers) =>
        prevModifiers.filter((modifier) => modifier.effect !== effectToRemove)
      );
    }
  };

  const handleCheckboxChange = (id: number) => {
    setSelectedModifiers((modifiers) =>
      modifiers.map((modifier) =>
        modifier.modifierId[0] === id
          ? { ...modifier, isSelected: !modifier.isSelected }
          : modifier
      )
    );
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const bottom =
      e.currentTarget.scrollHeight - e.currentTarget.scrollTop ===
      e.currentTarget.clientHeight;
    if (bottom && !isExpanded) {
      setIsExpanded(true);
    }
  };

  const updateModifierInput = (
    modifierId: number,
    newMinRollInputs?: (number | null)[] | undefined,
    newMaxRollInputs?: (number | null)[] | undefined,
    newTextRollInputs?: (string | null)[] | undefined
  ): void => {
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
  };

  // Define a function to check if an array has only null values
  function isArrayNullOrContainsOnlyNull<T>(
    arr: T[] | null | undefined
  ): boolean {
    if (arr === null || arr === undefined) {
      return true; // If the array is null, return true
    }
    // Check if every element in the array is null
    return arr.every((value) => value === null);
  }

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
                handleCheckboxChange(modifierSelected.modifierId[0]);
              }
            }}
          />
        </Center>

        <Center bgColor={"ui.secondary"} width={"100%"}>
          <Text ml={3} mr={"auto"}>
            {modifierSelected.effect}
          </Text>

          <Flex justifyContent="flex-end">
            {/* Check if modifierSelected static exists and is not all null */}
            {isArrayNullOrContainsOnlyNull(modifierSelected.static) &&
              (() => {
                const elements = [];
                for (
                  let modifierInputIndex = 0;
                  modifierInputIndex < modifierSelected.position.length;
                  modifierInputIndex++
                ) {
                  if (
                    !isArrayNullOrContainsOnlyNull(modifierSelected.minRoll) &&
                    modifierSelected.minRoll &&
                    modifierSelected.minRoll[modifierInputIndex] !== null
                  ) {
                    const selectedModifierInput =
                      modifierSelected?.minRollInputs
                        ? modifierSelected.minRollInputs[modifierInputIndex]
                        : undefined;

                    elements.push(
                      <MinRollInput
                        modifierSelected={modifierSelected}
                        input={selectedModifierInput}
                        inputPosition={modifierInputIndex}
                        updateModifierInputFunction={() =>
                          updateModifierInput(
                            modifierSelected.modifierId[0],
                            modifierSelected.minRollInputs
                          )
                        }
                        key={"minRollPosition" + index + modifierInputIndex}
                      />
                    );
                  }

                  if (
                    !isArrayNullOrContainsOnlyNull(modifierSelected.maxRoll) &&
                    modifierSelected.maxRoll &&
                    modifierSelected.maxRoll[modifierInputIndex] !== null
                  ) {
                    const selectedModifierInput =
                      modifierSelected?.maxRollInputs
                        ? modifierSelected.maxRollInputs[modifierInputIndex]
                        : undefined;

                    elements.push(
                      <MaxRollInput
                        modifierSelected={modifierSelected}
                        input={selectedModifierInput}
                        inputPosition={modifierInputIndex}
                        updateModifierInputFunction={() =>
                          updateModifierInput(
                            modifierSelected.modifierId[0],
                            undefined,
                            modifierSelected.maxRollInputs
                          )
                        }
                        key={"maxRollPosition" + index + modifierInputIndex}
                      />
                    );
                  }
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
                handleRemoveModifier(modifierSelected.modifierId[0]);
              }
            }}
          />
        </Center>
      </Flex>
    )
  );

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
          onChange={(e) => handleInputChange(e.target.value)}
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
            maxHeight="200px"
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
