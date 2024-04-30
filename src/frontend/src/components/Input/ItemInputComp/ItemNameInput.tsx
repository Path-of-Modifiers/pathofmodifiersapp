import { Input, Flex, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

const handleNameChange = (value: string) => {
  const itemNameInput = value;
  useGraphInputStore.setState({ itemSpecState: { name: itemNameInput } });
  console.log("ITEM NAME INPUT STORE");
  console.log(useGraphInputStore.getState().itemSpecState);
};

export const ItemNameInput = () => {
  return (
    <Flex
      color={"ui.white"}
      bgColor={"ui.secondary"}
      alignItems={"center"}
      m={1}
    >
      <Text ml={1} width={150}>Item name</Text>
      <Input
        bgColor={"ui.input"}
        color={"ui.white"}
        defaultValue={""}
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
