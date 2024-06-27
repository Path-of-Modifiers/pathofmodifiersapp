import { Flex } from "@chakra-ui/layout";
import { IsItemInput } from "./ItemInputComp/IsItemInput";
import { MinMaxInput } from "./ItemInputComp/MinMaxItemLvlInput";
import { useEffect } from "react";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { AddICheckText } from "../Icon/AddICheckText";
import { useExpandedComponentStore } from "../../store/ExpandedComponentStore";

// Miscellaneous Item Input Component  -  This component is used to input miscellaneous item properties.
export const MiscItemInput = () => {
  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const miscItemExpanded = useExpandedComponentStore(
    (state) => state.expandedMiscItem
  );

  const { setExpandedMiscItem } = useExpandedComponentStore();

  const handleExpanded = () => {
    setExpandedMiscItem(!miscItemExpanded);
  };

  useEffect(() => {
    if (clearClicked) {
      setExpandedMiscItem(false);
    }
  }, [clearClicked, setExpandedMiscItem]);

  return (
    <Flex direction={"column"} width={"inputSizes.lgBox"}>
      <AddICheckText
        isChecked={miscItemExpanded}
        onChange={handleExpanded}
        text="Miscellaneous"
      />
      {miscItemExpanded && (
        <Flex flexWrap={"wrap"} justifyContent={"flex-start"} gap={2} ml={10}>
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
          <IsItemInput itemSpecKey={"replica"} text={"Replica"} />
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
