import {
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
} from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

const handleChange = (eventValue: string, itemSpecKey: string) => {
  const eventValueInt = parseInt(eventValue);

  switch (itemSpecKey) {
    case "minIlvl":
      useGraphInputStore.setState({
        itemSpecState: { minIlvl: eventValueInt },
      });
      break;
    case "maxIlvl":
      useGraphInputStore.setState({
        itemSpecState: { maxIlvl: eventValueInt },
      });
      break;
    case "foilVariation":
      useGraphInputStore.setState({
        itemSpecState: { foilVariation: eventValueInt },
      });
      break;
  }
};

export const NumberItemInput = (itemSpecKey: string) => {
  return (
    <NumberInput
      step={1}
      key={itemSpecKey + "_number_item_input"}
      bgColor={"ui.input"}
      focusBorderColor={"ui.white"}
      borderColor={"ui.grey"}
      onChange={(e) => handleChange(e, itemSpecKey)}
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
  );
};
