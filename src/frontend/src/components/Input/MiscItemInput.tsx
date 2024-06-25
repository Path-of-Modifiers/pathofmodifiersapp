import { Box, Flex, Text } from "@chakra-ui/layout";
import { IsItemInput } from "./ItemInputComp/IsItemInput";
import { MinMaxInput } from "./ItemInputComp/MinMaxItemLvlInput";
import { useEffect, useState } from "react";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { AddIconCheckbox } from "../Icon/AddIconCheckbox";

// Miscellaneous Item Input Component  -  This component is used to input miscellaneous item properties.
export const MiscItemInput = () => {
  const [miscExpanded, setMiscExpanded] = useState(false);

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleExpanded = () => {
    setMiscExpanded(!miscExpanded);
  };

  useEffect(() => {
    if (clearClicked) {
      setMiscExpanded(false);
    }
  }, [clearClicked]);

  return (
    <Flex direction={"column"} width={"inputSizes.lgBox"}>
      <Flex gap={2} alignItems={"center"}>
        <AddIconCheckbox isChecked={miscExpanded} onChange={handleExpanded} />

        <Box flex="1" position="relative">
          <Text color={"ui.white"}>Miscellaneous</Text>
          <Box
            position="absolute"
            top="1"
            bottom="0"
            left="0"
            right="0"
            borderBottom="1px solid"
            borderColor="ui.grey"
          />
        </Box>
      </Flex>
      {miscExpanded && (
        <Flex flexWrap={"wrap"} justifyContent={"flex-start"} gap={2} ml={6}>
          <IsItemInput itemSpecKey={"identified"} text={"Identified"} />
          <IsItemInput itemSpecKey={"corrupted"} text={"Corrupted"} />
          <MinMaxInput
            itemMinSpecKey="minIlvl"
            itemMaxSpecKey="maxIlvl"
            text="Item level"
          />
          <IsItemInput itemSpecKey={"delve"} text={"Delve"} />
          <IsItemInput itemSpecKey={"fractured"} text={"Fracture"} />
          <IsItemInput itemSpecKey={"synthesized"} text={"Synthesize"} />
          <IsItemInput itemSpecKey={"replica"} text={"Replic"} />
          <IsItemInput itemSpecKey={"searing"} text={"Exarch influence"} />
          <IsItemInput itemSpecKey={"tangled"} text={"Eater influence"} />
          <IsItemInput itemSpecKey={"elder"} text={"Elder influence"} />
          <IsItemInput itemSpecKey={"shaper"} text={"Shaper influence"} />
          <IsItemInput itemSpecKey={"crusader"} text={"Crusader influence"} />
          <IsItemInput itemSpecKey={"redeemer"} text={"Redeemer influence"} />
          <IsItemInput itemSpecKey={"hunter"} text={"Hunter influence"} />
          <IsItemInput itemSpecKey={"warlord"} text={"Warlord influence"} />
          <IsItemInput itemSpecKey={"isRelic"} text={"Relic"} />
        </Flex>
      )}
    </Flex>
  );
};
