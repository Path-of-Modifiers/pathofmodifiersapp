import {
  Flex,
  Text,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
} from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

const handleMaxChange = (eventValue: string, itemSpecKey: string) => {
  const eventValueInt = parseInt(eventValue);

  switch (itemSpecKey) {
    case "maxIlvl":
      useGraphInputStore.setState({
        itemSpecState: { maxIlvl: eventValueInt },
      });
      break;
  }
};

const handleMinChange = (eventValue: string, itemSpecKey: string) => {
  const eventValueInt = parseInt(eventValue);

  switch (itemSpecKey) {
    case "minIlvl":
      useGraphInputStore.setState({
        itemSpecState: { minIlvl: eventValueInt },
      });
      break;
  }
};

interface MinMaxInputProps {
  itemMinSpecKey: string;
  itemMaxSpecKey: string;
  text: string;
}

export const MinMaxInput = ({
  itemMinSpecKey,
  itemMaxSpecKey,
  text,
}: MinMaxInputProps) => {
  return (
    <Flex
      color={"ui.white"}
      m={2}
      ml={1}
      bgColor={"ui.secondary"}
      alignItems={"center"}
    >
      <Text ml={1} width={150}>
        {text}
      </Text>
      <NumberInput
        value={undefined}
        step={1}
        key={"itemSpecKey" + "min_number_input"}
        bgColor={"ui.input"}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        onChange={(e) => handleMinChange(e, itemMinSpecKey)}
        width={150}
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
        value={undefined}
        step={1}
        key={"MinMaxInput" + "max_number_item_input"}
        bgColor={"ui.input"}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        onChange={(e) => handleMaxChange(e, itemMaxSpecKey)}
        width={150}
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
