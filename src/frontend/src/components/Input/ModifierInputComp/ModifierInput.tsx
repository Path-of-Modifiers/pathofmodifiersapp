import { Center, CloseButton, Flex, Stack } from "@chakra-ui/react";

import AddIconCheckbox from "../../Icon/AddIconCheckbox";

import { useEffect, useState } from "react";
import { GroupedModifierByEffect } from "../../../client";
import { TextRollInput } from "./TextRollInput";
import { MinMaxRollInput } from "./MinMaxRollInput";
import {
  getEventTextContent,
  isArrayNullOrContainsOnlyNull,
} from "../../../hooks/utils";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { GetGroupedModifiersByEffect } from "../../../hooks/getGroupedModifiers";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";
import { useOutsideClick } from "../../../hooks/useOutsideClick";

export interface ModifierInput extends GroupedModifierByEffect {
  isSelected?: boolean;
  minRollInputs?: (number | null)[];
  maxRollInputs?: (number | null)[];
  textRollInputs?: (number | null)[];
}

export const ModifierInput = () => {
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

  const { addModifierSpec, removeModifierSpec } = useGraphInputStore();

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const modifiers: ModifierInput[] | undefined = GetGroupedModifiersByEffect();

  const defaultValue = undefined;

  const mappedFilteredOptionsList: Array<SelectBoxOptionValue> =
    filteredModifiers.map((modifier) => {
      return {
        value: modifier.effect,
        text: modifier.effect,
      };
    });

  // Filter the modifiers based on the search text and selected modifiers.
  useEffect(() => {
    if (modifiers) {
      const filtered = modifiers.filter(
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
    };

    if (clearClicked) {
      clearAllModifiers();
    }
  }, [selectedModifiers, modifiers, clearClicked]);

  // Define the reference to the outside click hook. This is used to close the dropdown when clicking outside of it.
  const ref = useOutsideClick(() => {
    const store = useGraphInputStore.getState();
    console.log("STORE", store);
  });

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

  const handleModifierSelect = (
    e: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>,
    replaceModifierInput?: ModifierInput
  ) => {
    const selectedModifierEffect = modifiers?.find(
      (modifier) => modifier.effect === getEventTextContent(e)
    );

    if (!selectedModifierEffect) {
      return;
    }

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

    // Remove the replaceModifierInput
    if (replaceModifierInput) {
      handleRemoveModifier(
        replaceModifierInput.modifierId[0],
        replaceModifierInput
      );
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

  // Render selected modifiers list
  const selectedModifiersList = selectedModifiers.map(
    (modifierSelected, index) => (
      <Flex
        key={index}
        bgColor={"ui.main"}
        flexDirection={"row"}
        height={10}
        maxHeight={10}
        maxWidth="inputSizes.ultraBox"
        alignItems={"center"}
      >
        <Center minWidth="inputSizes.miniBox">
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

        <SelectBoxInput
          handleChange={(e) => handleModifierSelect(e, modifierSelected)}
          optionsList={mappedFilteredOptionsList}
          defaultText={modifierSelected.effect}
          defaultValue={modifierSelected.effect}
          itemKeyId="modifierInputItem"
          onFocusNotBlankInputText={true}
          width={"inputSizes.xlPlusBox"}
        />

        <Flex ml="auto">
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
                  modifierSelected.minRoll[modifierInputIndex] !== null &&
                  modifierSelected.maxRoll &&
                  modifierSelected.maxRoll[modifierInputIndex] !== null
                ) {
                  elements.push(
                    <MinMaxRollInput
                      modifierSelected={modifierSelected}
                      inputPosition={modifierInputIndex}
                      key={"minRollPosition" + index + modifierInputIndex}
                    />
                  );
                }

                // Check if textRolls exists and is not all null. If so, create a TextRollInput component
                if (
                  !isArrayNullOrContainsOnlyNull(modifierSelected.textRolls) &&
                  modifierSelected.textRolls &&
                  modifierSelected.textRolls[modifierInputIndex] !== null
                ) {
                  elements.push(
                    <TextRollInput
                      modifierSelected={modifierSelected}
                      inputPosition={modifierInputIndex}
                      key={"textRollPosition" + index + modifierInputIndex}
                    />
                  );
                }
              }
              return elements;
            })()}

          <Center minWidth="inputSizes.miniBox">
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
      </Flex>
    )
  );

  return (
    <Flex direction="column" color="ui.dark">
      <Stack color={"ui.white"} mb={2} ref={ref} width={"inputSizes.ultraBox"}>
        {selectedModifiersList}
      </Stack>

      <SelectBoxInput
        handleChange={(e) => handleModifierSelect(e)}
        optionsList={mappedFilteredOptionsList}
        defaultText=""
        defaultValue={defaultValue}
        itemKeyId="modifierInput"
        width="inputSizes.ultraBox"
        staticPlaceholder="+ Add modifier"
        centerInputText={true}
      />
    </Flex>
  );
};
