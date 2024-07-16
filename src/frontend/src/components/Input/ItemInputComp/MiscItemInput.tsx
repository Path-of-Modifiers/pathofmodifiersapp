import { Flex } from "@chakra-ui/layout";
import { IsItemInput } from "./IsItemProp";
import { MinMaxInput } from "./MinMaxProp";
import { useEffect, useState } from "react";
import { Checkbox, CheckboxIcon, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

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
    <Flex direction={"column"}>
      <Flex>
        <Checkbox isChecked={miscExpanded} onChange={handleExpanded}>
          <CheckboxIcon />
        </Checkbox>
        <Text color={"ui.white"}>Miscellaneous</Text>
      </Flex>
      {miscExpanded && (
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
