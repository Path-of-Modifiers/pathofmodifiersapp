import { Input } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

const handleNameChange = (value: string) => {
  const itemNameInput = value;
  useGraphInputStore.setState({ itemSpecState: { name: itemNameInput } });
  console.log("ITEM NAME INPUT STORE");
  console.log(useGraphInputStore.getState().itemSpecState);
};

export const ItemNameInput = () => {
  return (
    <Input
      bgColor={"ui.input"}
      color={"ui.white"}
      defaultValue={""}
      onChange={(e) => handleNameChange(e.target.value)}
      width={150}
      focusBorderColor={"ui.white"}
      placeholder="Item Name"
      borderColor={"ui.grey"}
      mr={1}
      ml={1}
      key={"ItemRarityInput"}
    />
  );
};
