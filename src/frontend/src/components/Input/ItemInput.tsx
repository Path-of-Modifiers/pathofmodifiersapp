import { Box, Flex } from "@chakra-ui/layout";
import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";
import { IsItemInput } from "./ItemInputComp/IsItemProp";
import { MinMaxInput } from "./ItemInputComp/MinMaxProp";
import { useState } from "react";
import { Checkbox, CheckboxIcon, Text } from "@chakra-ui/react";
import { isExternal } from "util/types";

export const ItemInput = () => {
  const [influenceExpanded, setInfluenceExpanded] = useState(false);

  const handleExpanded = () => {
    console.log("EXPANDED");
    setInfluenceExpanded(!influenceExpanded);
  };

  return (
    <Flex direction={"column"}>
      <ItemNameInput />
      <ItemRarityInput />
      <IsItemInput itemSpecKey={"identified"} text={"Identified"} />

      <Flex>
        <Checkbox onChange={handleExpanded}>
          <CheckboxIcon />
        </Checkbox>
        <Text color={"ui.white"}>Miscellaneous</Text>
      </Flex>
      {influenceExpanded && (
        <Flex flexWrap={"wrap"} width={650}>
          <IsItemInput itemSpecKey={"corrupted"} text={"Corrupted"} />
          <MinMaxInput
            itemMinSpecKey="minIlvl"
            itemMaxSpecKey="maxIlvl"
            text="Item level"
          />
          <IsItemInput itemSpecKey={"delve"} text={"Delve item"} />
          <IsItemInput itemSpecKey={"fractured"} text={"Fractured item"} />
          <IsItemInput itemSpecKey={"synthesized"} text={"Synthesized item"} />
          <IsItemInput itemSpecKey={"replica"} text={"Replica item"} />
          <IsItemInput itemSpecKey={"searing"} text={"Exarch influence item"} />
          <IsItemInput itemSpecKey={"tangled"} text={"Eater influence item"} />
          <IsItemInput itemSpecKey={"elder"} text={"Elder influence item"} />
          <IsItemInput itemSpecKey={"shaper"} text={"Shaper influence item"} />
          <IsItemInput
            itemSpecKey={"crusader"}
            text={"Crusader influence item"}
          />
          <IsItemInput
            itemSpecKey={"redeemer"}
            text={"Redeemer influence item"}
          />
          <IsItemInput itemSpecKey={"hunter"} text={"Hunter influence item"} />
          <IsItemInput
            itemSpecKey={"warlord"}
            text={"Warlord influence item"}
          />
          <IsItemInput itemSpecKey={"isRelic"} text={"Relic item"} />
        </Flex>
      )}
    </Flex>
  );
};
