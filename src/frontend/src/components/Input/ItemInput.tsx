import { Flex } from "@chakra-ui/layout";
import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";
import { IsItemInput } from "./ItemInputComp/IsItemProp";
import { MinMaxInput } from "./ItemInputComp/MinMaxProp";

export const ItemInput = () => {
  return (
    <Flex direction={"column"}>
      <ItemNameInput />
      <ItemRarityInput />
      <IsItemInput itemSpecKey={"identified"} text={"Identified"} />
      <IsItemInput itemSpecKey={"corrupted"} text={"Corrupted"} />
      <IsItemInput itemSpecKey={"delve"} text={"Delve item"} />
      <IsItemInput itemSpecKey={"fractured"} text={"Fractured item"} />
      <IsItemInput itemSpecKey={"synthesized"} text={"Synthesized item"} />
      <IsItemInput itemSpecKey={"replica"} text={"Replica item"} />
      <IsItemInput itemSpecKey={"searing"} text={"Exarch influence item"} />
      <IsItemInput itemSpecKey={"tangled"} text={"Eater influence item"} />
      <IsItemInput itemSpecKey={"elder"} text={"Elder influence item"} />
      <IsItemInput itemSpecKey={"shaper"} text={"Shaper influence item"} />
      <IsItemInput itemSpecKey={"crusader"} text={"Crusader influence item"} />
      <IsItemInput itemSpecKey={"redeemer"} text={"Redeemer influence item"} />
      <IsItemInput itemSpecKey={"hunter"} text={"Hunter influence item"} />
      <IsItemInput itemSpecKey={"warlord"} text={"Warlord influence item"} />
      <IsItemInput itemSpecKey={"isRelic"} text={"Relic item"} />
      <MinMaxInput
        itemMinSpecKey="minIlvl"
        itemMaxSpecKey="maxIlvl"
        text="Item level"
      />
    </Flex>
  );
};
