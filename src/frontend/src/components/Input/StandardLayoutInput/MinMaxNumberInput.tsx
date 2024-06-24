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
  width?: string | number;
  height?: string | number;
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
  width,
  height,
}: MinMaxNumberInputProps) => {
  const initialMinValue = useRef(getMinValue());
  const initialMaxValue = useRef(getMaxValue());

  return (
    <Flex
      color={"ui.white"}
      width={width || "inputSizes.smallPPBox"}
      height={height || "lineHeights.tall"}
      flexDirection={"column"}
    >
      {descriptionText && (
        <Text mb={2} fontSize={15}>
          {descriptionText}
        </Text>
      )}

      <Flex>
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
          _placeholder={{ color: "ui.white" }}
          textAlign={"center"}
        >
          <NumberInputField pl={2} placeholder={"Min"} bgColor="ui.input" />
          <NumberInputStepper width="inputSizes.tinyBox">
            <NumberIncrementStepper color="ui.grey" />
            <NumberDecrementStepper color="ui.grey" />
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
          _placeholder={{ color: "ui.white" }}
          textAlign={"center"}
        >
          <NumberInputField pl={2} placeholder={"Max"} bgColor="ui.input" />
          <NumberInputStepper width="inputSizes.tinyBox">
            <NumberIncrementStepper color="ui.grey" />
            <NumberDecrementStepper color="ui.grey" />
          </NumberInputStepper>
        </NumberInput>
      </Flex>
    </Flex>
  );
};
