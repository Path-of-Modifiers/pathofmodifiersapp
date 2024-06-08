import { Input, Flex, Text } from "@chakra-ui/react";
import {
  GetValueFunction,
  HandleChangeStringFunction,
} from "../../../schemas/function/InputFunction";

interface TextInputProps {
  getTextValue: GetValueFunction;
  handleTextChange: HandleChangeStringFunction;
}

// Item Name Input Component  -  This component is used to input the name of an item.
export const TextInput = ({
  getTextValue,
  handleTextChange,
}: TextInputProps) => {
  return (
    <Flex
      color={"ui.white"}
      bgColor={"ui.secondary"}
      alignItems={"center"}
      m={1}
    >
      <Text ml={1} width={"inputSizes.defaultDescriptionText"}>
        Item name
      </Text>
      <Input
        value={getTextValue()}
        bgColor={"ui.input"}
        color={"ui.white"}
        onChange={(e) => handleTextChange(e.target.value)}
        width={"inputSizes.lgBox"}
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
