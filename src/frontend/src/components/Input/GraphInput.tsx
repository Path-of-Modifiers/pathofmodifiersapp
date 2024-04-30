import { Box } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInput";
import { ItemInput } from "./ItemInput";

export const GraphInput = () => {
  return (
    <Box p={5}>
      <ItemInput />
      <ModifierInput />
    </Box>
  );
};
