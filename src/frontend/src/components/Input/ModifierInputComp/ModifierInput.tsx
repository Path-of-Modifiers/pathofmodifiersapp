import { Box, CloseButton, Flex, Stack } from "@chakra-ui/react";

import AddIconCheckbox from "../../Icon/AddIconCheckbox";

// For debugging purposes
import { useOutsideClick } from "../../../hooks/useOutsideClick";

import { useEffect, useState } from "react";
import { GroupedModifierByEffect } from "../../../client";
import { TextRollInput } from "./TextRollInput";
import { MinMaxRollInput } from "./MinMaxRollInput";
import {
  getEventTextContent,
  isArrayNullOrContainsOnlyNull,
} from "../../../hooks/utils";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";
import { AddICheckText } from "../../Icon/AddICheckText";
import { ModifierSpecState } from "../../../store/StateInterface";
import { useExpandedComponentStore } from "../../../store/ExpandedComponentStore";

export interface SelectedModifier extends GroupedModifierByEffect {
  isSelected?: boolean;
  minRollInputs?: (number | null)[];
  maxRollInputs?: (number | null)[];
  textRollInputs?: (number | null)[];
}

interface ModifierInputProps {
  prefetchedmodifiers: GroupedModifierByEffect[];
}

export const ModifierInput = (props: ModifierInputProps) => {
  const [filteredModifiers, setFilteredModifiers] = useState<
    SelectedModifier[]
  >([
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

  const [selectedModifiers, setSelectedModifiers] = useState<
    SelectedModifier[]
  >([]);

  const { addModifierSpec, removeModifierSpec } = useGraphInputStore();

  const { setExpandedModifiers } = useExpandedComponentStore();

  const expandedModifiers = useExpandedComponentStore(
    (state) => state.expandedModifiers
  );

  const globalModifierSpecs = useGraphInputStore(
    (state) => state.modifierSpecs
  );

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const modifiers: SelectedModifier[] | undefined = props.prefetchedmodifiers;

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

    // Define the function to find a modifier in modifiers list by its modifierId
    const findModifierByModifierId = (
      modifierId: number
    ): SelectedModifier | undefined => {
      if (modifiers && modifiers.length > 0) {
        const modifier = modifiers.find(
          (modifier) => modifier.modifierId[0] === modifierId
        );
        return modifier;
      } else {
        return undefined;
      }
    };

    const getSelectedModifierFromModifierSpec = (
      modifierSpec: ModifierSpecState
    ) => {
      const selectedModifier = findModifierByModifierId(
        modifierSpec.modifierId
      );
      if (selectedModifier) {
        selectedModifier.isSelected = true;
        const minRolls = modifierSpec.modifierLimitations?.minRoll;
        const maxRolls = modifierSpec.modifierLimitations?.maxRoll;
        const textRolls = modifierSpec.modifierLimitations?.textRoll;
        if (minRolls) {
          selectedModifier.minRollInputs = new Array(
            selectedModifier.position.length
          ).fill(undefined);
        }
        if (maxRolls) {
          selectedModifier.maxRollInputs = new Array(
            selectedModifier.position.length
          ).fill(undefined);
        }
        if (textRolls) {
          selectedModifier.textRollInputs = new Array(
            selectedModifier.position.length
          ).fill(undefined);
        }
        for (let i = 0; i < selectedModifier.position.length; i++) {
          if (minRolls && selectedModifier.minRollInputs !== undefined) {
            selectedModifier.minRollInputs[i] = minRolls;
          }
          if (maxRolls && selectedModifier.maxRollInputs !== undefined) {
            selectedModifier.maxRollInputs[i] = maxRolls;
          }
          if (textRolls && selectedModifier.textRollInputs !== undefined) {
            selectedModifier.textRollInputs[i] = textRolls;
          }
        }
        return selectedModifier;
      } else {
        return undefined;
      }
    };

    if (globalModifierSpecs.length > 0 && selectedModifiers.length === 0) {
      const selectedModifiersList = globalModifierSpecs
        .map(getSelectedModifierFromModifierSpec)
        .filter(Boolean) as SelectedModifier[];
      setSelectedModifiers(selectedModifiersList);
    }

    const clearAllModifiers = () => {
      setSelectedModifiers([]);
    };

    if (clearClicked) {
      clearAllModifiers();
      setExpandedModifiers(false);
    }
  }, [
    selectedModifiers,
    modifiers,
    clearClicked,
    globalModifierSpecs,
    setExpandedModifiers,
  ]);

  // For debugging purposes
  const ref = useOutsideClick(() => {
    const store = useGraphInputStore.getState();
    console.log("STORE", store);
    console.log("LOCALSTORESELECTEDMODIFIERS", selectedModifiers);
  });

  const handleExpanded = () => {
    setExpandedModifiers(!expandedModifiers);
  };

  const getSelectModifierTextValue = (modifier: SelectedModifier) => {
    if (modifier) {
      return modifier.effect;
    } else {
      return "";
    }
  };

  // Define the function to remove a selected modifier
  const handleRemoveModifier = (modifierSelected: SelectedModifier) => {
    const modifierToRemove = selectedModifiers.find(
      (modifier) => modifier.modifierId[0] === modifierSelected.modifierId[0]
    )?.effect;

    // Remove the selected modifier from the selectedModifiers list if it exists
    if (modifierToRemove) {
      setSelectedModifiers((prevModifiers) =>
        prevModifiers.filter((modifier) => modifier.effect !== modifierToRemove)
      );

      // Remove the modifier from the global state store
      for (let i = 0; i < modifierSelected.position.length; i++) {
        removeModifierSpec(modifierSelected.modifierId[i]);
      }
    }
  };

  const handleModifierSelect = (
    e: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>,
    positionToSelect?: number,
    replaceSelectedModifier?: SelectedModifier
  ) => {
    const effectSelected = getEventTextContent(e);
    const selectedModifier = modifiers?.find(
      (modifier) => modifier.effect === effectSelected
    );

    if (!selectedModifier) {
      return;
    }

    // Set the clicked modifier as selected
    selectedModifier.isSelected = true;
    // Set selected modifiers at the position if positionToSelect is defined
    if (positionToSelect !== undefined) {
      setSelectedModifiers((selectedModifiers) => [
        ...selectedModifiers.slice(0, positionToSelect),
        selectedModifier,
        ...selectedModifiers.slice(positionToSelect),
      ]);
    } else {
      setSelectedModifiers((selectedModifiers) => [
        ...selectedModifiers,
        selectedModifier,
      ]);
    }

    // Initialize the input arrays for the selected modifier
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifier.minRoll) &&
      selectedModifier.minRoll
    ) {
      selectedModifier.minRollInputs = new Array(
        selectedModifier.minRoll.length
      ).fill(undefined);
    }
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifier.maxRoll) &&
      selectedModifier.maxRoll
    ) {
      selectedModifier.maxRollInputs = new Array(
        selectedModifier.maxRoll.length
      ).fill(undefined);
    }
    if (
      !isArrayNullOrContainsOnlyNull(selectedModifier.textRolls) &&
      selectedModifier.textRolls
    ) {
      selectedModifier.textRollInputs = new Array(
        selectedModifier.textRolls.length
      ).fill(undefined);
    }

    // Remove the replaceSelectedModifier
    if (replaceSelectedModifier) {
      handleRemoveModifier(replaceSelectedModifier);
    }

    const addModifier = (
      modifier: typeof selectedModifier,
      position: number
    ) => {
      addModifierSpec(
        {
          modifierId: modifier.modifierId[position],
          position: modifier.position[position],
          modifierLimitations: {
            minRoll: modifier.minRollInputs
              ? modifier.minRollInputs[position]
              : null,
            maxRoll: modifier.maxRollInputs
              ? modifier.maxRollInputs[position]
              : null,
            textRoll: modifier.textRollInputs
              ? modifier.textRollInputs[position]
              : null,
          },
        },
        positionToSelect ?? undefined
      );
    };

    // Add the selected modifier(s) to the global state store
    for (let i = 0; i < selectedModifier.position.length; i++) {
      addModifier(selectedModifier, i);
    }
  };

  // Define the function to handle checkbox changes for the selected modifiers
  const handleCheckboxChange = (
    modifierId: number,
    modifierSelected: SelectedModifier,
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
        alignItems={"center"}
        gap={2}
      >
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

        <SelectBoxInput
          handleChange={(e) => handleModifierSelect(e, index, modifierSelected)}
          optionsList={mappedFilteredOptionsList}
          defaultText={modifierSelected.effect}
          defaultValue={modifierSelected.effect}
          itemKeyId="selectedModifierItem"
          getSelectTextValue={getSelectModifierTextValue(modifierSelected)}
          onFocusNotBlankInputText={true}
          isDimmed={!modifierSelected.isSelected}
          width={"inputSizes.xlPlusBox"}
          noInputChange={true}
          key={"inputbox" + modifierSelected.effect + index}
        />

        <Flex ml="auto" gap={2}>
          {/* Check if modifierSelected static exists and is all null */}
          {isArrayNullOrContainsOnlyNull(modifierSelected.static) &&
            (() => {
              const elements = [];
              for (
                let selectedModifierIndex = 0;
                selectedModifierIndex < modifierSelected.position.length;
                selectedModifierIndex++
              ) {
                // Check if minRoll exists and are not all null. If so, create a MinRollInput component
                if (
                  !isArrayNullOrContainsOnlyNull(modifierSelected.minRoll) &&
                  modifierSelected.minRoll &&
                  modifierSelected.minRoll[selectedModifierIndex] !== null &&
                  modifierSelected.maxRoll &&
                  modifierSelected.maxRoll[selectedModifierIndex] !== null
                ) {
                  elements.push(
                    <MinMaxRollInput
                      modifierSelected={modifierSelected}
                      inputPosition={selectedModifierIndex}
                      key={"minRollPosition" + index + selectedModifierIndex}
                    />
                  );
                }

                // Check if textRolls exists and is not all null. If so, create a TextRollInput component
                if (
                  !isArrayNullOrContainsOnlyNull(modifierSelected.textRolls) &&
                  modifierSelected.textRolls &&
                  modifierSelected.textRolls[selectedModifierIndex] !== null
                ) {
                  elements.push(
                    <TextRollInput
                      modifierSelected={modifierSelected}
                      inputPosition={selectedModifierIndex}
                      key={"textRollPosition" + index + selectedModifierIndex}
                    />
                  );
                }
              }
              return elements;
            })()}

          <CloseButton
            _hover={{ background: "gray.100", cursor: "pointer" }}
            onClick={() => {
              if (modifierSelected.modifierId[0] !== null) {
                handleRemoveModifier(modifierSelected);
              }
            }}
          />
        </Flex>
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
            {selectedModifiersList}
          </Stack>

          {/* mx here needs to be same length as checkboxes in selectedModifiersList */}
          <Box
            mx={"40px"}
            mr={"40px"}
            // For debugging purposes
            ref={ref}
          >
            <SelectBoxInput
              handleChange={(e) => handleModifierSelect(e)}
              optionsList={mappedFilteredOptionsList}
              defaultText=""
              defaultValue={defaultValue}
              getSelectTextValue=""
              width="100%"
              itemKeyId="selectedModifier"
              staticPlaceholder="+ Add modifier"
              centerInputText={true}
              noInputChange={true}
            />
          </Box>
        </Box>
      )}
    </Flex>
  );
};
