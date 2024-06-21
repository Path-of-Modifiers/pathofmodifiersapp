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
import { useRef } from "react";

interface MinMaxNumberInputProps {
  descriptionText?: string;
  minSpecKey: string;
  maxSpecKey: string;
  getMinValue: GetValueFunction;
  getMaxValue: GetValueFunction;
  handleMinChange: HandleChangeStringFunction;
  handleMaxChange: HandleChangeStringFunction;
}

// Min Max Item Lvl Input Component  -  This component is used to input the min and max ilvl of an item.
export const MinMaxNumberInput = ({
  descriptionText,
  minSpecKey,
  maxSpecKey,
  getMinValue,
  getMaxValue,
  handleMinChange,
  handleMaxChange,
}: MinMaxNumberInputProps) => {
  const initialMinValue = useRef(getMinValue());
  const initialMaxValue = useRef(getMaxValue());

  return (
    <Flex color={"ui.white"} m={2} ml={1} alignItems={"center"}>
      <Text ml={1} width={"inputSizes.defaultDescriptionText"}>
        {descriptionText}
      </Text>
      <NumberInput
        value={getMinValue() ?? ""}
        step={1}
        key={minSpecKey}
        borderWidth={getMinValue() !== initialMinValue.current ? 1 : 0}
        borderRadius={getMinValue() !== initialMinValue.current ? 9 : 0}
        borderColor={
          getMinValue() !== initialMinValue.current
            ? "ui.inputChanged"
            : "ui.grey"
        }
        precision={0}
        focusBorderColor={"ui.white"}
        onChange={(e) => handleMinChange(e)}
        width={"inputSizes.defaultBox"}
        mr={1}
        ml={1}
        _placeholder={{ color: "ui.white" }}
        textAlign={"center"}
      >
        <NumberInputField placeholder={"Min"} bgColor="ui.input" />
        <NumberInputStepper>
          <NumberIncrementStepper />
          <NumberDecrementStepper />
        </NumberInputStepper>
      </NumberInput>

      <NumberInput
        value={getMaxValue() ?? ""}
        step={1}
        key={maxSpecKey}
        borderWidth={getMaxValue() !== initialMaxValue.current ? 1 : 0}
        borderRadius={getMaxValue() !== initialMaxValue.current ? 9 : 0}
        focusBorderColor={"ui.white"}
        borderColor={
          getMaxValue() !== initialMaxValue.current
            ? "ui.inputChanged"
            : "ui.grey"
        }
        onChange={(e) => handleMaxChange(e)}
        width={"inputSizes.defaultBox"}
        mr={1}
        ml={1}
        _placeholder={{ color: "ui.white" }}
        textAlign={"center"}
      >
        <NumberInputField placeholder={"Max"} bgColor="ui.input" />
        <NumberInputStepper>
          <NumberIncrementStepper />
          <NumberDecrementStepper />
        </NumberInputStepper>
      </NumberInput>
    </Flex>
  );
};
