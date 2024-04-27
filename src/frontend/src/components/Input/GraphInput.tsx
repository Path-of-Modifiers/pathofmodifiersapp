import { Box } from "@chakra-ui/react";
import { ItemRarityInput } from "./ItemRarityInput";
import { ModifierInput } from "./ModifierInput";

export const GraphInput = () => {
  return (
    <Box>
      <ItemRarityInput />
      <ModifierInput />
    </Box>
  );
};
