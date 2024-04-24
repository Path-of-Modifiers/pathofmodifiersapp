import {
  Box,
  CloseButton,
  Flex,
  Input,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  Select,
  Stack,
  Text,
} from "@chakra-ui/react";

import AddIconCheckbox from "../Icon/AddIconCheckbox";

import { useEffect, useState } from "react";
import { GroupedModifierByEffect } from "../../client";
import { useOutsideClick } from "../../hooks/useOutsideClick";
import React from "react";
import { modifiers } from "../../test_data/modifier_data";
// import { GetGroupedModifiersByEffect } from "../../hooks/getGroupedModifiers";

const ModiferInput = () => {
  return <ModifierListInput />;
};

interface ModifierInput extends GroupedModifierByEffect {
  isSelected?: boolean;
  minRollInputs?: (number | null)[];
  maxRollInputs?: (number | null)[];
  textRollInputs?: (string | null)[];
}

function ModifierListInput() {
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

  // Define types for input cases
  type InputCase = "modifier" | "minPosition" | "maxPosition" | "textPosition";

  // Define the function to handle input changes
  const handleInputChange = (
    value: string,
    inputCase: InputCase,
    position?: number,
    modifier?: ModifierInput
  ) => {
    // Regular expression to allow numbers and scientific notation
    // const scientificPattern = /^-?\d*\.?\d*(e-?\d+)?$/i;

    if (inputCase === "modifier") {
      setSearchModifierText(value);
    }
    if (!modifier || position === undefined || position < 0) {
      return;
    }
    switch (inputCase) {
      case "minPosition":
        if (modifier.minRollInputs) {
          modifier.minRollInputs[position] = parseInt(value);
        } else {
          modifier.minRollInputs = [parseInt(value)];
        }
        updateModifierInput(
          modifier.modifierId[position],
          modifier.minRollInputs
        );
        break;
      case "maxPosition":
        if (modifier.maxRollInputs) {
          modifier.maxRollInputs[position] = parseInt(value);
        } else {
          modifier.maxRollInputs = [parseInt(value)];
        }
        updateModifierInput(
          modifier.modifierId[position],
          undefined,
          modifier.maxRollInputs,
          undefined
        );
        break;
      case "textPosition":
        if (modifier.textRollInputs) {
          modifier.textRollInputs[position] = value;
        } else {
          modifier.textRollInputs = [value];
        }
        updateModifierInput(
          modifier.modifierId[position],
          undefined,
          undefined,
          modifier.textRollInputs
        );
        break;
      default:
        // Handle default case
        break;
    }
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
          modifierToUpdate.minRollInputs = newMinRollInputs; // Update minRollInputs
        } else if (newMaxRollInputs) {
          modifierToUpdate.maxRollInputs = newMaxRollInputs;
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

  interface RenderInputProps {
    modifierSelected: ModifierInput;
    input: string | number | undefined | null;
    handleInputChangeCase: InputCase;
    inputPosition: number;
    key: string;
  }

  const renderInputBasedOnConditions = ({
    modifierSelected,
    input,
    handleInputChangeCase,
    inputPosition,
    key,
  }: RenderInputProps): JSX.Element | null => {
    const selectedModifierInput = selectedModifiers.find(
      (selectedModifier) =>
        selectedModifier.modifierId[0] === modifierSelected.modifierId[0]
    );

    if (selectedModifierInput) {
      const handleChange = (
        event:
          | React.ChangeEvent<HTMLInputElement>
          | React.ChangeEvent<HTMLSelectElement>
          | string
          | number
      ) => {
        if (typeof event === "string" || typeof event === "number") {
          event = {
            target: { value: event },
          } as React.ChangeEvent<HTMLInputElement>;
        }
        const selectedValue = event.target.value;
        // Call function to handle the change
        handleInputChange(
          selectedValue,
          handleInputChangeCase,
          inputPosition,
          modifierSelected
        );
      };

      // Access the specific property of the ModifierInput object based on handleInputChangeCase
      if (
        handleInputChangeCase === "minPosition" &&
        selectedModifierInput.minRollInputs &&
        modifierSelected.minRoll
      ) {
        const defaultValue = modifierSelected.minRoll[inputPosition] as number;

        return (
          <NumberInput
            value={input ? input : defaultValue}
            defaultValue={defaultValue}
            step={1}
            key={key}
            bgColor={"ui.input"}
            focusBorderColor={"ui.white"}
            borderColor={"ui.grey"}
            onChange={handleChange}
            width={"30%"}
            _placeholder={{ color: "ui.white" }}
            textAlign={"center"}
          >
            <NumberInputField />
            <NumberInputStepper>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        );
      }
      if (
        handleInputChangeCase === "maxPosition" &&
        selectedModifierInput.maxRollInputs &&
        selectedModifierInput.maxRoll
      ) {
        const defaultValue = selectedModifierInput.maxRoll[
          inputPosition
        ] as number;

        if (input === 0) {
          input = defaultValue;
        }

        return (
          <NumberInput
            value={input ? input : 0}
            defaultValue={defaultValue}
            step={1}
            key={key}
            bgColor={"ui.input"}
            onChange={handleChange}
            focusBorderColor={"ui.white"}
            borderColor={"ui.grey"}
            width={"30%"}
            _placeholder={{ color: "ui.white" }}
            textAlign={"center"}
          >
            <NumberInputField />
            <NumberInputStepper textColor={"ui.white"}>
              <NumberIncrementStepper />
              <NumberDecrementStepper />
            </NumberInputStepper>
          </NumberInput>
        );
      }
      if (
        handleInputChangeCase === "textPosition" &&
        !isArrayNullOrContainsOnlyNull(modifierSelected.textRolls) &&
        modifierSelected.textRolls
      ) {
        const textRolls = modifierSelected.textRolls[inputPosition] as string;
        const textRollsList = textRolls.split("-");

        const textRollsOptions = textRollsList.map((textRoll, index) => (
          <option
            value={textRoll}
            key={key + textRoll + index}
            style={{ backgroundColor: "#2d3333" }}
          >
            {textRoll}
          </option>
        ));

        return (
          <Select
            bgColor={"ui.input"}
            defaultValue={"TextRolls"}
            onChange={handleChange}
            focusBorderColor={"ui.white"}
            borderColor={"ui.grey"}
            width={"40%"}
            key={key}
          >
            {textRollsOptions}
          </Select>
        );
      }
    }
    return null;
  };

  // Render selected modifiers list
  const selectedModifiersList = selectedModifiers.map(
    (modifierSelected, index) => (
      <Flex key={index} alignItems="center" bgColor={"ui.secondary"}>
        <Box bgColor={"ui.main"} width={8} height={8}>
          <AddIconCheckbox
            isChecked={modifierSelected.isSelected}
            top={"24%"}
            left={"24%"}
            key={modifierSelected.modifierId[0] + index}
            onChange={() => {
              if (modifierSelected.modifierId[0] !== null) {
                handleCheckboxChange(modifierSelected.modifierId[0]);
              }
            }}
          />
        </Box>

        <Text ml={3} mr={"auto"}>
          {modifierSelected.effect}
        </Text>

        <Flex width={"35%"} justifyContent="flex-end" ml={"auto"}>
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
                  const selectedModifierInput = modifierSelected?.minRollInputs
                    ? modifierSelected.minRollInputs[modifierInputIndex]
                    : undefined;

                  elements.push(
                    renderInputBasedOnConditions({
                      modifierSelected: modifierSelected,
                      input: selectedModifierInput,
                      handleInputChangeCase: "minPosition" as InputCase,
                      inputPosition: modifierInputIndex,
                      key: "minPosition" + index + modifierInputIndex,
                    })
                  );
                }

                if (
                  !isArrayNullOrContainsOnlyNull(modifierSelected.maxRoll) &&
                  modifierSelected.maxRoll &&
                  modifierSelected.maxRoll[modifierInputIndex] !== null
                ) {
                  const selectedModifierInput = modifierSelected?.maxRollInputs
                    ? modifierSelected.maxRollInputs[modifierInputIndex]
                    : undefined;

                  elements.push(
                    renderInputBasedOnConditions({
                      modifierSelected: modifierSelected,
                      input: selectedModifierInput,
                      handleInputChangeCase: "maxPosition" as InputCase,
                      inputPosition: modifierInputIndex,
                      key: "maxPosition" + index + modifierInputIndex,
                    })
                  );
                }
                if (
                  !isArrayNullOrContainsOnlyNull(modifierSelected.textRolls) &&
                  modifierSelected.textRolls &&
                  modifierSelected.textRolls[modifierInputIndex] !== null
                ) {
                  const selectedModifierInput = modifierSelected?.textRollInputs
                    ? modifierSelected.textRollInputs[modifierInputIndex]
                    : undefined;

                  elements.push(
                    renderInputBasedOnConditions({
                      modifierSelected: modifierSelected,
                      input: selectedModifierInput,
                      handleInputChangeCase: "textPosition" as InputCase,
                      inputPosition: modifierInputIndex,
                      key: "textPosition" + index + modifierInputIndex,
                    })
                  );
                }
              }
              return elements;
            })()}
        </Flex>

        <Box bgColor={"ui.main"}>
          <CloseButton
            _hover={{ background: "gray.100", cursor: "pointer" }}
            onClick={() => {
              if (modifierSelected.modifierId[0] !== null) {
                handleRemoveModifier(modifierSelected.modifierId[0]);
              }
            }}
          />
        </Box>
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
          onChange={(e) => handleInputChange(e.target.value, "modifier")}
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
      {/* <Input
        placeholder="Enter a modifier"
        value={effectValueSearchInput}
        onChange={(e) => setEffectValueSearchInput(e.target.value)}
        width="200px"
        color={"ui.white"}
      /> */}

      {/* 
      <Menu>
        <MenuButton bgColor={"ui.white"} color={"ui.dark"}>
          Filter by Effect
        </MenuButton>
        <MenuList color={"ui.dark"} maxHeight="200px" overflowY="auto">
          {effects.map((effect, index) => (
            <MenuItem
              color={"ui.dark"}
              key={index}
              onClick={() => setEffectValueList(effect)}
            >
              {effect === effectValueList ? "✓" : ""} {effect}
            </MenuItem>
          ))}
        </MenuList>
      </Menu> */}
    </Flex>
  );
}

export default ModiferInput;
