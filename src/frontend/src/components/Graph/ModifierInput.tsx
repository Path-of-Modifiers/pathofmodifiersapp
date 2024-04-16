import {
  Box,
  Checkbox,
  CloseButton,
  Flex,
  Input,
  Stack,
  Text,
} from "@chakra-ui/react";

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

  const filteredModifierEffects: ModifierEffect[] = filteredModifiers.map(
    (modifier) => ({
      modifierId: modifier.modifierId,
      effect: modifier.effect,
      isSelected: false,
    })
  );

  const ref = useOutsideClick(() => {
    setIsExpanded(false);
  });

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchText(event.target.value);
  };

  const handleModifierSelect = (selectedModifierEffect: ModifierEffect) => {
    if (
      !selectedModifiers.some(
        (modifierEffect) =>
          modifierEffect.modifierId === selectedModifierEffect.modifierId
      )
    ) {
      setSelectedModifiers([...selectedModifiers, selectedModifierEffect]);
    }
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

  const handleInputBlur = (event: React.FocusEvent<HTMLInputElement>) => {
    console.log(event.target.className);
    if (event.target.className.includes("modifiers-list")) {
      return;
    }
    if (isExpanded) {
      setIsExpanded(false);
    }
  };

  const selectedModifiersList = selectedModifiers.map((modifier) => (
    <Flex key={modifier.modifierId} alignItems="center">
      <Checkbox
        isChecked={modifier.isSelected}
        onChange={() => handleCheckboxChange(modifier.modifierId)}
      />
      <Text ml={2}>{modifier.effect}</Text>
      <CloseButton
        ml={2}
        onClick={() => handleRemoveModifier(modifier.modifierId)}
      />
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
    <Flex direction="column" color="ui.dark" width={500}>
      <Box bgColor={"ui.white"} ref={ref}>
        <Input
          className="modifiers-list"
          value={searchText}
          onChange={handleInputChange}
          placeholder="Search modifiers..."
          onFocus={() => {
            if (!isExpanded) {
              toggleExpand();
            }
          }}
          onBlur={handleInputBlur}
        />

        {isExpanded && (
          <Stack
            mt={2}
            maxHeight="200px"
            overflowY="auto"
            onScroll={handleScroll}
          >
            {modifiersList}
          </Stack>
        )}

        <Stack mt={2}>{selectedModifiersList}</Stack>
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
