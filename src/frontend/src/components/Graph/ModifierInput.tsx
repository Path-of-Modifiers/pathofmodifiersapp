import { Input, Menu, MenuButton, MenuItem, MenuList } from "@chakra-ui/react";

import { useState } from "react";
import { Modifier, ModifiersService } from "../../client";
import { useQuery } from "@tanstack/react-query";

const ModiferInput = () => {
  return <ModifierListInput />;
};

const GetModifiers = () => {
  let modifiers = [
    {
      position: 0,
      effect: "",
      createdAt: "",
      updatedAt: "",
    },
  ] as Modifier | Modifier[];

  try {
    useQuery({
      queryKey: ["allModifiers"],
      queryFn: async () => {
        modifiers = await ModifiersService.getAllModifiersApiApiV1ModifierGet();
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

function ModifierListInput() {
  const [effectValueSearchInpuut, setEffectValueSearchInput] = useState("");
  const [effectValueList, setEffectValueList] = useState("");

  const modifiers = GetModifiers();

  if (modifiers === undefined) {
    return <div>Error retrieving modifiers</div>;
  }

  const effects: Array<string> = Array.from(
    new Set(modifiers.map((modifier: Modifier) => modifier.effect))
  );

  return (
    <>
      <Input
        placeholder="Enter a modifier"
        value={effectValueSearchInpuut}
        onChange={(e) => setEffectValueSearchInput(e.target.value)}
      />

      <Menu>
        <MenuButton>Filter by Effect</MenuButton>
        <MenuList maxHeight="200px" overflowY="auto">
          {effects.map((effect, index) => (
            <MenuItem key={index} onClick={() => setEffectValueList(effect)}>
              {effect === effectValueList ? "✓" : ""} {effect}
            </MenuItem>
          ))}
        </MenuList>
      </Menu>
    </>
  );
}

export default ModiferInput;