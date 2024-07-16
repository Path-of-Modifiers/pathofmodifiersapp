import {
  Flex,
  Text,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
} from "@chakra-ui/react";
import {
  GetValueFunction,
  HandleChangeStringFunction,
} from "../../../schemas/function/InputFunction";

interface MinMaxNumberInputProps {
  text: string;
  minSpecKey: string;
  maxSpecKey: string;
  getMinValue: GetValueFunction;
  getMaxValue: GetValueFunction;
  handleMinChange: HandleChangeStringFunction;
  handleMaxChange: HandleChangeStringFunction;
}

// Min Max Item Lvl Input Component  -  This component is used to input the min and max ilvl of an item.
export const MinMaxNumberInput = ({
  text,
  minSpecKey,
  maxSpecKey,
  getMinValue,
  getMaxValue,
  handleMinChange,
  handleMaxChange,
}: MinMaxNumberInputProps) => {
  return (
    <Flex
      color={"ui.white"}
      m={2}
      ml={1}
      bgColor={"ui.secondary"}
      alignItems={"center"}
    >
      <Text ml={1} width={"inputSizes.defaultDescriptionText"}>
        {text}
      </Text>
      <NumberInput
        value={getMinValue()}
        step={1}
        key={minSpecKey}
        bgColor={"ui.input"}
        precision={0}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        onChange={(e) => handleMinChange(e)}
        width={"inputSizes.defaultBox"}
        mr={1}
        ml={1}
        _placeholder={{ color: "ui.white" }}
        textAlign={"center"}
      >
        <NumberInputField placeholder={"Min"} />
        <NumberInputStepper>
          <NumberIncrementStepper />
          <NumberDecrementStepper />
        </NumberInputStepper>
      </NumberInput>

      <NumberInput
        value={getMaxValue()}
        step={1}
        key={maxSpecKey}
        bgColor={"ui.input"}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        onChange={(e) => handleMaxChange(e)}
        width={"inputSizes.defaultBox"}
        mr={1}
        ml={1}
        _placeholder={{ color: "ui.white" }}
        textAlign={"center"}
      >
        <NumberInputField placeholder={"Max"} />
        <NumberInputStepper>
          <NumberIncrementStepper />
          <NumberDecrementStepper />
        </NumberInputStepper>
      </NumberInput>
    </Flex>
  );
};
