import { Input, Menu, MenuButton, MenuItem, MenuList } from "@chakra-ui/react";

import {
  QueryClient,
  QueryClientProvider,
  useQuery,
} from "@tanstack/react-query";
import { useState } from "react";
import { Modifier } from "../../client";

const queryClient = new QueryClient();

const ModiferInput = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <GetModifiers />
    </QueryClientProvider>
  );
};

function GetModifiers() {
  const [effectValueSearchInpuut, setEffectValueSearchInput] = useState("");
  const [effectValueList, setEffectValueList] = useState("");

  const { isPending, error, data } = useQuery({
    queryKey: ["modifiers"],
    queryFn: () =>
      fetch("http://localhost/api/api_v1/modifier/").then((res) => res.json()),
  });

  console.log(data);

  const effects: Array<string> = Array.from(
    new Set(data.map((modifier: Modifier) => modifier.effect))
  );

  if (isPending) return "Loading...";

  if (error) return "An error has occurred: " + error.message;

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
