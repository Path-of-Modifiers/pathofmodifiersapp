import {
  Box,
  Checkbox,
  CloseButton,
  Flex,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";

import AddIconCheckbox from "../Icon/AddIconCheckbox";

import { useState } from "react";
import { Modifier } from "../../client";
import { useQuery } from "@tanstack/react-query";
import { useOutsideClick } from "../../hooks/useOutsideClick";

const ModiferInput = () => {
  return <ModifierListInput />;
};

const GetModifiers = () => {
  let modifiers = [
    {
      position: 0,
      effect: "Could not retrieve modifiers...",
      createdAt: "",
      updatedAt: "",
    },
  ] as Modifier | Modifier[];

  try {
    useQuery({
      queryKey: ["allModifiers"],
      queryFn: async () => {
        // modifiers = await ModifiersService.getAllModifiersApiApiV1ModifierGet();
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

interface ModifierEffect {
  modifierId: number;
  effect: string;
  min_roll_position_one?: number;
  max_roll_position_one?: number;
  min_roll_position_two?: number;
  max_roll_position_two?: number;
  text_roll_position_one?: string;
  text_roll_position_two?: string;
  isSelected?: boolean;
}

function ModifierListInput() {
  const [searchText, setSearchText] = useState("");
  const [selectedModifiers, setSelectedModifiers] = useState<ModifierEffect[]>(
    []
  );
  const [isExpanded, setIsExpanded] = useState(false);

  const modifiers: Modifier[] | undefined = GetModifiers();
  const testModifiers: Modifier[] = [
    {
      modifierId: 6,
      position: 0,
      minRoll: 15.0,
      maxRoll: 20.0,
      textRolls: null,
      static: null,
      effect: "#% increased Armour",
      regex: "([+-]?([0-9]*[.])?[0-9]+)% (increased|reduced) Armour",
      implicit: null,
      explicit: null,
      delve: null,
      fractured: null,
      synthesized: null,
      unique: true,
      corrupted: null,
      enchanted: null,
      veiled: null,
      createdAt: "2024-04-15T14:32:49.651728",
      updatedAt: "2024-04-15T14:32:49.651766",
    },
    {
      modifierId: 7,
      position: 0,
      minRoll: 15.0,
      maxRoll: 20.0,
      textRolls: null,
      static: null,
      effect: "#% increased Evasion Rating",
      regex: "([+-]?([0-9]*[.])?[0-9]+)% (increased|reduced) Evasion Rating",
      implicit: null,
      explicit: null,
      delve: null,
      fractured: null,
      synthesized: null,
      unique: true,
      corrupted: null,
      enchanted: null,
      veiled: null,
      createdAt: "2024-04-15T14:32:49.651728",
      updatedAt: "2024-04-15T14:32:49.651766",
    },
    {
      modifierId: 10,
      position: 0,
      minRoll: null,
      maxRoll: null,
      textRolls:
        "Anger-Clarity-Determination-Discipline-Grace-Haste-Purity of Elements-Purity of Fire-Purity of Ice-Purity of Lightning-Vitality-Wrath-Envy-Malevolence-Zealotry-Pride",
      static: null,
      effect: "# has no Reservation",
      regex:
        "(Anger|Clarity|Determination|Discipline|Grace|Haste|Purity of Elements|Purity of Fire|Purity of Ice|Purity of Lightning|Vitality|Wrath|Envy|Malevolence|Zealotry|Pride) has no Reservation",
      implicit: null,
      explicit: null,
      delve: null,
      fractured: null,
      synthesized: null,
      unique: true,
      corrupted: null,
      enchanted: null,
      veiled: null,
      createdAt: "2024-04-15T14:32:49.651728",
      updatedAt: "2024-04-15T14:32:49.651766",
    },
    {
      modifierId: 11,
      position: 0,
      minRoll: null,
      maxRoll: null,
      textRolls: "Xibaqua-Xopec-Xoph-Xoph's Blood",
      static: true,
      effect:
        "Hits against Nearby Enemies have 50% increased Critical Strike Chance",
      regex: null,
      implicit: null,
      explicit: null,
      delve: null,
      fractured: null,
      synthesized: null,
      unique: true,
      corrupted: null,
      enchanted: null,
      veiled: null,
      createdAt: "2024-04-15T14:32:49.651728",
      updatedAt: "2024-04-15T14:32:49.651766",
    },
    {
      modifierId: 12,
      position: 1,
      minRoll: 34,
      maxRoll: 67,
      textRolls: null,
      static: true,
      effect:
        "Hits against Nearby Enemies have 50% increased Critical Strike Chance",
      regex: null,
      implicit: null,
      explicit: null,
      delve: null,
      fractured: null,
      synthesized: null,
      unique: true,
      corrupted: null,
      enchanted: null,
      veiled: null,
      createdAt: "2024-04-15T14:32:49.651728",
      updatedAt: "2024-04-15T14:32:49.651766",
    },
  ];

  const filteredModifiers: Modifier[] = testModifiers
    .filter((modifier) =>
      modifier.effect.toLowerCase().includes(searchText.toLowerCase())
    )
    .filter(
      (modifier) =>
        !selectedModifiers.some((m) => m.modifierId === modifier.modifierId)
    );

  // Group modifiers by effect
  const groupedModifiers = filteredModifiers.reduce<{
    [effect: string]: Modifier[];
  }>((acc, modifier) => {
    const effect = modifier.effect;
    acc[effect] = acc[effect] || [];
    acc[effect].push(modifier);
    return acc;
  }, {});

  const filteredModifierEffects: ModifierEffect[] = [];

  // Process each group
  for (const modifiers of Object.values(groupedModifiers)) {
    const positionOne: Partial<ModifierEffect> = {};
    const positionTwo: Partial<ModifierEffect> = {};

    for (const modifier of modifiers) {
      if (modifier.position === 0) {
        if (modifier.minRoll && modifier.maxRoll) {
          positionOne.min_roll_position_one = modifier.minRoll;
          positionOne.max_roll_position_one = modifier.maxRoll;
        } else if (modifier.textRolls) {
          positionOne.text_roll_position_one = modifier.textRolls;
        }
      } else if (modifier.position === 1) {
        if (modifier.minRoll && modifier.maxRoll) {
          positionTwo.min_roll_position_two = modifier.minRoll;
          positionTwo.max_roll_position_two = modifier.maxRoll;
        } else if (modifier.textRolls) {
          positionTwo.text_roll_position_two = modifier.textRolls;
        }
      }
    }

    filteredModifierEffects.push({
      modifierId: modifiers[0].modifierId,
      effect: modifiers[0].effect,
      isSelected: false,
      ...positionOne,
      ...positionTwo,
    });
  }

  // const filteredModifierEffects: ModifierEffect[] = filteredModifiers.map(
  //   (modifier) => ({
  //     modifierId: modifier.modifierId,
  //     effect: modifier.effect,
  //     min_roll_position_one: modifier.minRoll,
  //     max_roll_position_one: modifier.maxRoll,
  //     min_roll_position_two: modifier.minRoll,
  //     max_roll_position_two: modifier.maxRoll,
  //     text_roll_position_one: modifier.textRolls,
  //     text_roll_position_two: modifier.textRolls,
  //     isSelected: false,
  //   })
  // );

  const ref = useOutsideClick(() => {
    setIsExpanded(false);
    console.log("Selected modifiers: \n");
    console.log(selectedModifiers);
    console.log("Filtered modifiers: \n");
    console.log(filteredModifierEffects);
    console.log("Grouped modifiers: \n");
    console.log(groupedModifiers);
  });

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(event.target.value);
  };

  const handleModifierSelect = (selectedModifierEffect: ModifierEffect) => {
    // Set the clicked modifier as selected
    selectedModifierEffect.isSelected = true;

    // Find all modifiers with the same effect
    const modifiersWithSameEffect =
      groupedModifiers[selectedModifierEffect.effect];

    // Mark all modifiers with the same effect as selected
    modifiersWithSameEffect.forEach((modifier) => {
      if (
        !selectedModifiers.some((m) => m.modifierId === modifier.modifierId)
      ) {
        setSelectedModifiers((prevModifiers) => [
          ...prevModifiers,
          {
            modifierId: modifier.modifierId,
            effect: modifier.effect,
            isSelected: true,
            // Add other properties if needed
          },
        ]);
      }
    });

    setSearchText("");
  };

  const handleRemoveModifier = (id: number) => {
    setSelectedModifiers(
      selectedModifiers.filter((modifier) => modifier.modifierId !== id)
    );
  };
  const handleCheckboxChange = (id: number) => {
    setSelectedModifiers(
      selectedModifiers.map((modifier) =>
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

  const selectedModifiersList = selectedModifiers.map((modifierEffect) => (
    <Flex
      key={modifierEffect.modifierId}
      alignItems="center"
      bgColor={"ui.secondary"}
    >
      <Box bgColor={"ui.main"} width={8} height={8}>
        <AddIconCheckbox
          isChecked={modifierEffect.isSelected}
          top={"24%"}
          left={"24%"}
          onChange={() => handleCheckboxChange(modifierEffect.modifierId)}
        />
      </Box>

      <Text ml={3}>{modifierEffect.effect}</Text>

      {modifierEffect.min_roll_position_one &&
        modifierEffect.max_roll_position_one && (
          <Text ml={3}>
            {modifierEffect.min_roll_position_one} -{" "}
            {modifierEffect.max_roll_position_one}
          </Text>
        )}

      <Box ml={"auto"} bgColor={"ui.main"}>
        <CloseButton
          _hover={{ background: "gray.100", cursor: "pointer" }}
          onClick={() => handleRemoveModifier(modifierEffect.modifierId)}
        />
      </Box>
    </Flex>
  ));

  const modifiersList = filteredModifierEffects.map((modifier) => (
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
