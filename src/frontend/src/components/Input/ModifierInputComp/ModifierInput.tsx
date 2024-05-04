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

  const [isExpanded, setIsExpanded] = useState(false);

  const modifiers: ModifierInput[] | undefined = GetGroupedModifiersByEffect();

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
  }, [searchModifierText, selectedModifiers, modifiers]);

  const ref = useOutsideClick(() => {
    setIsExpanded(false);
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

    for (let i = 0; i < selectedModifierEffect.position.length; i++) {
      addModifierSpec({
        modifierId: selectedModifierEffect.modifierId[i],
        position: i,
        limitations: {
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

  const handleRemoveModifier = (
    modifierId: number,
    modifierSelected: ModifierInput
  ) => {
    const effectToRemove = selectedModifiers.find(
      (modifier) => modifier.modifierId[0] === modifierId
    )?.effect;

    if (effectToRemove) {
      setSelectedModifiers((prevModifiers) =>
        prevModifiers.filter((modifier) => modifier.effect !== effectToRemove)
      );
    }

    for (let i = 0; i < modifierSelected.position.length; i++) {
      removeModifierSpec(modifierSelected.modifierId[i]);
    }
  };

  const handleCheckboxChange = (
    id: number,
    modifierSelected: ModifierInput,
    modifierIsSelected: boolean | undefined
  ) => {
    setSelectedModifiers((modifiers) =>
      modifiers.map((modifier) =>
        modifier.modifierId[0] === id
          ? { ...modifier, isSelected: !modifier.isSelected }
          : modifier
      )
    );

    if (modifierIsSelected) {
      for (let i = 0; i < modifierSelected.position.length; i++) {
        removeModifierSpec(modifierSelected.modifierId[i]);
      }
    } else {
      for (let i = 0; i < modifierSelected.position.length; i++) {
        addModifierSpec({
          modifierId: id,
          position: modifierSelected.position[i],
          limitations: {
            minRoll: modifierSelected.minRollInputs?.[i] ?? null,
            maxRoll: modifierSelected.maxRollInputs?.[i] ?? null,
            textRoll: modifierSelected.textRollInputs?.[i] ?? null,
          },
        });
      }
    }
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
    modifierToUpdate: ModifierInput,
    newMinRollInputs?: (number | null)[] | undefined,
    newMaxRollInputs?: (number | null)[] | undefined,
    newTextRollInputs?: (number | null)[] | undefined
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

    for (let i = 0; i < modifierToUpdate.position.length; i++) {
      updateModifierSpec({
        modifierId: modifierToUpdate.modifierId[i],
        position: modifierToUpdate.position[i],
        limitations: {
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
                            modifierSelected,
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
                            modifierSelected,
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
