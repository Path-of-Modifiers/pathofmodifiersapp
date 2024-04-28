import { Box } from "@chakra-ui/react";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";
import { ModifierInput } from "./ModifierInput";
import { ItemInput } from "./ItemInput";

export const GraphInput = () => {
  return (
    <Box>
      <ItemInput/>
      <ItemRarityInput />
      <ModifierInput />
    </Box>
  );
};
