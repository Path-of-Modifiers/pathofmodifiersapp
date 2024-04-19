import {
  Box,
  CloseButton,
  Flex,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";

import AddIconCheckbox from "../Icon/AddIconCheckbox";

import { useState } from "react";
import { GroupedModifierByEffect, ModifiersService } from "../../client";
import { useQuery } from "@tanstack/react-query";
import { useOutsideClick } from "../../hooks/useOutsideClick";
import React from "react";

const ModiferInput = () => {
  return <ModifierListInput />;
};

const GetModifiers = () => {
  let modifiers = [
    {
      modifierId: [0],
      position: [0],
      minRoll: null,
      maxRoll: null,
      textRolls: null,
      effect: "",
      static: null,
    },
  ] as GroupedModifierByEffect | GroupedModifierByEffect[];

  try {
    useQuery({
      queryKey: ["allModifiers"],
      queryFn: async () => {
        modifiers =
          await ModifiersService.getGroupedModifierByEffectApiApiV1ModifierGroupedModifiersByEffectGet();
      },
    });
    if (Array.isArray(modifiers)) {
      return modifiers; // If modifiers is already an array, return it directly
    } else {
      return [modifiers]; // If modifiers is not an array, wrap it in an array
    }
  } catch (error) {
    console.log(error);
  }
};

interface ModifierInput {
  modifierId: Array<number>;
  position: Array<number>;
  minRoll?: null | undefined;
  maxRoll?: null | undefined;
  textRolls?: null | undefined;
  effect: string;
  static?: null | undefined;
  isSelected?: boolean;
}

function ModifierListInput() {
  const [searchText, setSearchText] = useState("");
  const [selectedModifiers, setSelectedModifiers] = useState<Modifier[]>([]);
  const [filteredModifiers, setFilteredModifiers] = useState<Modifier[]>([
    {
      modifierId: [0],
      position: [0],
      effect: "",
    },
  ]);
  const [isExpanded, setIsExpanded] = useState(false);

  const modifiers: Modifier[] | undefined = GetModifiers();
  // const testModifiers: Modifier[] = [
  //   {
  //     modifierId: 6,
  //     position: 0,
  //     minRoll: 15.0,
  //     maxRoll: 20.0,
  //     textRolls: null,
  //     static: null,
  //     effect: "#% increased Armour",
  //     regex: "([+-]?([0-9]*[.])?[0-9]+)% (increased|reduced) Armour",
  //     implicit: null,
  //     explicit: null,
  //     delve: null,
  //     fractured: null,
  //     synthesized: null,
  //     unique: true,
  //     corrupted: null,
  //     enchanted: null,
  //     veiled: null,
  //     createdAt: "2024-04-15T14:32:49.651728",
  //     updatedAt: "2024-04-15T14:32:49.651766",
  //   },
  //   {
  //     modifierId: 7,
  //     position: 0,
  //     minRoll: 15.0,
  //     maxRoll: 20.0,
  //     textRolls: null,
  //     static: null,
  //     effect: "#% increased Evasion Rating",
  //     regex: "([+-]?([0-9]*[.])?[0-9]+)% (increased|reduced) Evasion Rating",
  //     implicit: null,
  //     explicit: null,
  //     delve: null,
  //     fractured: null,
  //     synthesized: null,
  //     unique: true,
  //     corrupted: null,
  //     enchanted: null,
  //     veiled: null,
  //     createdAt: "2024-04-15T14:32:49.651728",
  //     updatedAt: "2024-04-15T14:32:49.651766",
  //   },
  //   {
  //     modifierId: 10,
  //     position: 0,
  //     minRoll: null,
  //     maxRoll: null,
  //     textRolls:
  //       "Anger-Clarity-Determination-Discipline-Grace-Haste-Purity of Elements-Purity of Fire-Purity of Ice-Purity of Lightning-Vitality-Wrath-Envy-Malevolence-Zealotry-Pride",
  //     static: null,
  //     effect: "# has no Reservation",
  //     regex:
  //       "(Anger|Clarity|Determination|Discipline|Grace|Haste|Purity of Elements|Purity of Fire|Purity of Ice|Purity of Lightning|Vitality|Wrath|Envy|Malevolence|Zealotry|Pride) has no Reservation",
  //     implicit: null,
  //     explicit: null,
  //     delve: null,
  //     fractured: null,
  //     synthesized: null,
  //     unique: true,
  //     corrupted: null,
  //     enchanted: null,
  //     veiled: null,
  //     createdAt: "2024-04-15T14:32:49.651728",
  //     updatedAt: "2024-04-15T14:32:49.651766",
  //   },
  //   {
  //     modifierId: 11,
  //     position: 0,
  //     minRoll: null,
  //     maxRoll: null,
  //     textRolls: "Xibaqua-Xopec-Xoph-Xoph's Blood",
  //     static: true,
  //     effect:
  //       "Hits against Nearby Enemies have 50% increased Critical Strike Chance",
  //     regex: null,
  //     implicit: null,
  //     explicit: null,
  //     delve: null,
  //     fractured: null,
  //     synthesized: null,
  //     unique: true,
  //     corrupted: null,
  //     enchanted: null,
  //     veiled: null,
  //     createdAt: "2024-04-15T14:32:49.651728",
  //     updatedAt: "2024-04-15T14:32:49.651766",
  //   },
  //   {
  //     modifierId: 12,
  //     position: 1,
  //     minRoll: 34,
  //     maxRoll: 67,
  //     textRolls: null,
  //     static: true,
  //     effect:
  //       "Hits against Nearby Enemies have 50% increased Critical Strike Chance",
  //     regex: null,
  //     implicit: null,
  //     explicit: null,
  //     delve: null,
  //     fractured: null,
  //     synthesized: null,
  //     unique: true,
  //     corrupted: null,
  //     enchanted: null,
  //     veiled: null,
  //     createdAt: "2024-04-15T14:32:49.651728",
  //     updatedAt: "2024-04-15T14:32:49.651766",
  //   },
  // ];

  if (modifiers) {
    setFilteredModifiers(
      modifiers
        .filter((modifier) =>
          modifier.effect.toLowerCase().includes(searchText.toLowerCase())
        )
        .filter(
          (modifier) =>
            !selectedModifiers.some((m) => m.modifierId === modifier.modifierId)
        )
    );
  }

  const ref = useOutsideClick(() => {
    setIsExpanded(false);
    console.log("Selected modifiers: \n");
    console.log(selectedModifiers);
    console.log("Filtered modifiers: \n");
    console.log(filteredModifiers);
  });

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(event.target.value);
  };

  const handleModifierSelect = (
    selectedModifierEffect: GroupedModifierByEffect
  ) => {
    // Set the clicked modifier as selected
    selectedModifierEffect.isSelected = true;
    setSelectedModifiers((prevModifiers) => [
      ...prevModifiers,
      selectedModifierEffect,
    ]);

    setSearchText("");
  };

  const handleRemoveModifier = (id: number) => {
    const effectToRemove = selectedModifiers.find(
      (modifier) => modifier.modifierId === id
    )?.effect;

    if (effectToRemove) {
      setSelectedModifiers((prevModifiers) =>
        prevModifiers.filter((modifier) => modifier.effect !== effectToRemove)
      );
    }
  };

  const handleCheckboxChange = (id: number) => {
    setSelectedModifiers((prevModifiers) =>
      prevModifiers.map((modifier) =>
        modifier.modifierId === id
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

  function groupSelectedModifiers(
    selectedModifiers: ModifierEffect[]
  ): ModifierEffect[][] {
    // Group selected modifiers by effect
    const groupedSelectedModifiers = selectedModifiers.reduce<{
      [effect: string]: ModifierEffect[];
    }>((acc, modifier) => {
      const effect = modifier.effect;
      acc[effect] = acc[effect] || [];
      acc[effect].push(modifier);
      return acc;
    }, {});

    // Convert object of arrays to array of arrays
    const groupedModifiersArray = Object.values(groupedSelectedModifiers);

    return groupedModifiersArray;
  }

  // Render selected modifiers list
  const selectedModifiersList = groupSelectedModifiers(selectedModifiers).map(
    (modifiersWithSameEffect, index) => (
      <Flex
        key={index} // You might want to use a more unique key here
        alignItems="center"
        bgColor={"ui.secondary"}
      >
        <Box bgColor={"ui.main"} width={8} height={8}>
          <AddIconCheckbox
            isChecked={modifiersWithSameEffect[0].isSelected}
            top={"24%"}
            left={"24%"}
            onChange={() =>
              handleCheckboxChange(modifiersWithSameEffect[0].modifierId)
            }
          />
        </Box>

        <Text ml={3}>{modifiersWithSameEffect[0].effect}</Text>

        {modifiersWithSameEffect.map((modifier, modifierIndex) => (
          <React.Fragment key={modifierIndex}>
            {modifier.min_roll_position_one != null &&
              modifier.max_roll_position_one != null && (
                <Text mr={"auto"} ml={3}>
                  YII
                </Text>
              )}
          </React.Fragment>
        ))}

        <Box ml={"auto"} bgColor={"ui.main"}>
          <CloseButton
            _hover={{ background: "gray.100", cursor: "pointer" }}
            onClick={() =>
              handleRemoveModifier(modifiersWithSameEffect[0].modifierId)
            }
          />
        </Box>
      </Flex>
    )
  );

  const modifiersList = generateFilteredModifierEffects().map((modifier) => (
    <Box
      key={modifier.modifierId}
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
          value={searchText}
          onChange={handleInputChange}
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
