import { Input, Flex, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

// Item Name Input Component  -  This component is used to input the name of an item.
export const ItemNameInput = () => {
  const { setItemName } = useGraphInputStore();

  const getItemNameValue = () => {
    const itemName = useGraphInputStore.getState().itemSpec.name;
    if (itemName) {
      return itemName;
    } else {
      return "";
    }
  };

  const handleNameChange = (value: string) => {
    const itemNameInput = value;
    setItemName(itemNameInput);
  };

  return (
    <Flex
      color={"ui.white"}
      bgColor={"ui.secondary"}
      alignItems={"center"}
      m={1}
    >
      <Text ml={1} width={150}>
        Item name
      </Text>
      <Input
        value={getItemNameValue()}
        bgColor={"ui.input"}
        color={"ui.white"}
        onChange={(e) => handleNameChange(e.target.value)}
        width={250}
        focusBorderColor={"ui.white"}
        placeholder="Item Name"
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"ItemRarityInput"}
      />
    </Flex>
  );
};
