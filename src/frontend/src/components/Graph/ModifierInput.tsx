import { Box, CloseButton, Flex, Input, Stack, Text } from "@chakra-ui/react";

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
  minRollInputs?: (number | null)[] | null;
  maxRollInputs?: (number | null)[] | null;
  textRollInputs?: (string | null)[] | null;
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
              (selectedModifier) => selectedModifier.effect === modifier.effect
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
    // console.log("Min roll position one: " + inputMinRollPositionOne);
    // console.log("Max roll position one: " + inputMaxRollPositionOne);
    // console.log("Min roll position two: " + inputMinRollPositionTwo);
    // console.log("Max roll position two: " + inputMaxRollPositionTwo);
    // console.log("Min roll position three: " + inputMinRollPositionThree);
    // console.log("Max roll position three: " + inputMaxRollPositionThree);
    // console.log("Text roll position one: " + inputTextRollPositionOne);
    // console.log("Text roll position two: " + inputTextRollPositionTwo);
  });

  // Define types for input cases
  type InputCase =
    | "modifier"
    | "minPosition1"
    | "maxPosition1"
    | "textPosition1"
    | "minPosition2"
    | "maxPosition2"
    | "textPosition2"
    | "minPosition3"
    | "maxPosition3"
    | "textPosition3";

  // Define the function to handle input changes
  const handleInputChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    inputCase: InputCase
  ) => {
    const value = event.target.value;
    // Regular expression to allow numbers and scientific notation
    // const scientificPattern = /^-?\d*\.?\d*(e-?\d+)?$/i;

    if (inputCase === "modifier") {
      setSearchModifierText(value);
      // }
      // if (scientificPattern.test(value) || value === "") {
      //   switch (inputCase) {
      //     // case "minPosition1":
      //     //   setInputMinRollPositionOne(value);
      //     //   break;
      //     // case "maxPosition1":
      //     //   setInputMaxRollPositionOne(value);
      //     //   break;
      //     // case "textPosition1":
      //     //   setInputTextRollPositionOne(value);
      //     //   break;
      //     // case "minPosition2":
      //     //   setInputMinRollPositionTwo(value);
      //     //   break;
      //     // case "maxPosition2":
      //     //   setInputMaxRollPositionTwo(value);
      //     //   break;
      //     // case "textPosition2":
      //     //   setInputTextRollPositionTwo(value);
      //     //   break;
      //     // case "minPosition3":
      //     //   setInputMinRollPositionThree(value);
      //     //   break;
      //     // case "maxPosition3":
      //     //   setInputMaxRollPositionThree(value);
      //     //   break;
      //     // case "textPosition3":
      //     //   setInputTextRollPositionThree(value);
      //     case
      //       break;
      //     default:
      //       // Handle default case
      //       break;
      //   }
    }
  };
  const handleModifierSelect = (selectedModifierEffect: ModifierInput) => {
    // Set the clicked modifier as selected
    selectedModifierEffect.isSelected = true;
    setSelectedModifiers((prevModifiers) => [
      ...prevModifiers,
      selectedModifierEffect,
    ]);

    setSearchModifierText("");
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

  // Define a function to check if an array has only null values
  function isArrayNullOrContainsOnlyNull<T>(
    arr: T[] | null | undefined
  ): boolean {
    if (arr === null) {
      return true; // If the array is null, return true
    }

    // Check if every element in the array is null
    if (arr === undefined) {
      return true;
    }
    return arr.every((value) => value === null);
  }

  interface RenderInputProps {
    input: (number | string | null)[] | null | undefined;
    inputValue: string;
    handleInputChangeCase: InputCase;
    width: string;
    position: number;
    placeholder: string;
    key: string;
  }

  const renderInputBasedOnConditions = ({
    input,
    inputValue,
    handleInputChangeCase,
    width,
    position,
    key,
    placeholder,
  }: RenderInputProps): JSX.Element | null => {
    if (
      !isArrayNullOrContainsOnlyNull(input) &&
      input !== null &&
      input !== undefined &&
      input[position] !== null
    ) {
      return (
        <Input
          value={inputValue}
          key={key}
          onChange={(e) => handleInputChange(e, handleInputChangeCase)}
          width={width}
          placeholder={placeholder}
          _placeholder={{ color: "ui.white" }}
          textAlign={"center"}
        />
      );
    }

    return null;
  };

  // Render selected modifiers list
  const selectedModifiersList = selectedModifiers.map((modifier, index) => (
    <Flex
      key={index} // You might want to use a more unique key here
      alignItems="center"
      bgColor={"ui.secondary"}
    >
      <Box bgColor={"ui.main"} width={8} height={8}>
        <AddIconCheckbox
          isChecked={modifier.isSelected}
          top={"24%"}
          left={"24%"}
          onChange={() => {
            if (modifier.modifierId[0] !== null) {
              handleCheckboxChange(modifier.modifierId[0]);
            }
          }}
        />
      </Box>

      <Text ml={3}>{modifier.effect}</Text>

      <React.Fragment key={index}>
        {/* Check if minRoll at position 1 exists and is not all null */}
        {/* Check if minRoll exists and is not all null */}
        {isArrayNullOrContainsOnlyNull(modifier.static) &&
          (() => {
            const elements = [];
            for (
              let modifierInputIndex = 0;
              modifierInputIndex < modifier.position.length;
              modifierInputIndex++
            ) {
              if (
                modifier.minRoll &&
                modifier.minRoll[modifierInputIndex] !== null &&
                modifier.minRoll[modifierInputIndex] !== undefined
              ) {
                elements.push(
                  renderInputBasedOnConditions({
                    input: modifier.minRoll,
                    inputValue: "minPosition" + modifierInputIndex,
                    handleInputChangeCase: ("minPosition" + index) as InputCase,
                    width: "10%",
                    position: modifierInputIndex,
                    placeholder: "MIN",
                    key: "minPosition" + modifierInputIndex,
                  })
                );
              }

              if (
                modifier.maxRoll &&
                modifier.maxRoll[modifierInputIndex] !== null &&
                modifier.maxRoll[modifierInputIndex] !== undefined
              ) {
                elements.push(
                  renderInputBasedOnConditions({
                    input: modifier.maxRoll,
                    inputValue: "maxPosition" + modifierInputIndex,
                    handleInputChangeCase: ("maxPosition" + index) as InputCase,
                    width: "10%",
                    position: modifierInputIndex,
                    key: "maxPosition" + modifierInputIndex,
                    placeholder: "MAX",
                  })
                );
                // setInputStates((prevInputStates) => ({
                //   ...prevInputStates,
                //   ["maxPosition" + modifierInputIndex]: modifier.maxRoll ? [modifierInputIndex].toString() : "",
                // }));
              }
              if (
                modifier.textRolls &&
                modifier.textRolls[modifierInputIndex] !== null &&
                modifier.textRolls[modifierInputIndex] !== undefined
              ) {
                elements.push(
                  renderInputBasedOnConditions({
                    input: modifier.textRolls,
                    inputValue: "textPosition" + modifierInputIndex,
                    handleInputChangeCase: ("textPosition" +
                      index) as InputCase,
                    width: "10%",
                    position: modifierInputIndex,
                    key: "textPosition" + modifierInputIndex,
                    placeholder: "TEXT",
                  })
                );
                // setInputStates((prevInputStates) => ({
                //   ...prevInputStates,
                //   ["textPosition" + modifierInputIndex]: modifier.textRolls ? [modifierInputIndex].toString() : "",
                // }));
              }
            }
            return elements;
          })()}
      </React.Fragment>

      {/* {selectedModifiers.map(
        (modifier_m2, index) =>
          !isArrayNullOrContainsOnlyNull(modifier_m2.minRoll[0]) &&
          !isArrayNullOrContainsOnlyNull(modifier_m2.maxRoll) && (
            <React.Fragment key={index}>
              <Input
                value={searchModifierText}
                onChange={handleInputChange}
                width={"10%"}
                placeholder="MIN"
                _placeholder={{ color: "ui.white" }}
                textAlign={"center"}
              />
              <Input
                value={searchModifierText}
                onChange={handleInputChange}
                width={"10%"}
                placeholder="MAX"
                _placeholder={{ color: "ui.white" }}
                textAlign={"center"}
              />
            </React.Fragment>
          )
      )} */}

      <Box ml={"auto"} bgColor={"ui.main"}>
        <CloseButton
          _hover={{ background: "gray.100", cursor: "pointer" }}
          onClick={() => {
            if (modifier.modifierId[0] !== null) {
              handleRemoveModifier(modifier.modifierId[0]);
            }
          }}
        />
      </Box>
    </Flex>
  ));

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
    <Flex direction="column" color="ui.dark" width={900}>
      <Stack color={"ui.white"} mb={2}>
        {selectedModifiersList}
      </Stack>

      <Box bgColor={"ui.input"} color={"ui.white"} ref={ref} mr={8} ml={8}>
        <Input
          value={searchModifierText}
          onChange={(e) => handleInputChange(e, "modifier")}
          placeholder="+ Add modifier"
          _placeholder={{ color: "ui.white" }}
          textAlign={"center"}
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
