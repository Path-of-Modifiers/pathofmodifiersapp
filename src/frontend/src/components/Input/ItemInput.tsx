import { Flex, Text } from "@chakra-ui/layout";
import { useEffect, useState } from "react";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { AddIconCheckbox } from "../Icon/AddIconCheckbox";
import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";

// Miscellaneous Item Input Component  -  This component is used to input miscellaneous item properties.
export const ItemInput = () => {
  const [itemInputExpanded, setItemInputExpanded] = useState(false);

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleExpanded = () => {
    setItemInputExpanded(!itemInputExpanded);
  };

  useEffect(() => {
    if (clearClicked) {
      setItemInputExpanded(false);
    }
  }, [clearClicked]);

  return (
    <Flex direction={"column"}>
      <Flex>
        <AddIconCheckbox
          isChecked={itemInputExpanded}
          onChange={handleExpanded}
        />
        <Text color={"ui.white"}>Item filters</Text>
      </Flex>
      {itemInputExpanded && (
        <Flex flexWrap={"wrap"} width={650}>
          <ItemNameInput />
          <ItemRarityInput />
        </Flex>
      )}
    </Flex>
  );
};
