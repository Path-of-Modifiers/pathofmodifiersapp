import { Box } from "@chakra-ui/react";
import { ModifierInput } from "./ModifierInput";
import { MiscItemInput } from "./MiscItemInput";
import { BaseInput } from "./BaseInput";
import { IsItemInput } from "./ItemInputComp/IsItemProp";
import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";
import { LeagueInput } from "./LeagueInput";

export const GraphInput = () => {
  return (
    <Box p={5}>
      <LeagueInput />
      <ItemNameInput />
      <ItemRarityInput />
      <IsItemInput itemSpecKey={"identified"} text={"Identified"} />
      <BaseInput />
      <MiscItemInput />
      <ModifierInput />
    </Box>
  );
};
