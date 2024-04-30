import { Box } from "@chakra-ui/react";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";
import { ModifierInput } from "./ModifierInput";
import { ItemInput } from "./ItemInput";
import { IsItemInput } from "./ItemInputComp/IsItemProp";
import { MinMaxInput } from "./ItemInputComp/MinMaxProp";

export const GraphInput = () => {
  return (
    <Box p={5}>
      <ItemInput />
      <ModifierInput />
    </Box>
  );
};
