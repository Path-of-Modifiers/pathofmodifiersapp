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

interface MinMaxInputProps {
  itemMinSpecKey: string;
  itemMaxSpecKey: string;
  text: string;
}

// Min Max Item Lvl Input Component  -  This component is used to input the min and max ilvl of an item.
export const MinMaxInput = ({ text }: MinMaxInputProps) => {
  const { setItemSpecMinIlvl, setItemSpecMaxIlvl } = useGraphInputStore();

  const [minValue, maxValue] = useGraphInputStore((state) => [
    state.itemSpecState.minIlvl,
    state.itemSpecState.maxIlvl,
  ]);

  const getMinValue = () => {
    if (minValue) {
      return minValue?.toString();
    } else {
      return "";
    }
  };

  const getMaxValue = () => {
    if (maxValue) {
      return maxValue?.toString();
    } else {
      return "";
    }
  };

  const handleMinChange = (eventValue: string) => {
    const eventValueInt = parseInt(eventValue);

    setItemSpecMinIlvl(eventValueInt);
  };

  const handleMaxChange = (eventValue: string) => {
    const eventValueInt = parseInt(eventValue);

    setItemSpecMaxIlvl(eventValueInt);
  };

  // useEffect(() => {}, [clearClicked]);

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
        value={getMinValue()}
        step={1}
        key={"itemSpecKey" + "min_number_input"}
        bgColor={"ui.input"}
        precision={0}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        onChange={(e) => handleMinChange(e)}
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
        value={getMaxValue()}
        step={1}
        key={"MinMaxInput" + "max_number_item_input"}
        bgColor={"ui.input"}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        onChange={(e) => handleMaxChange(e)}
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
