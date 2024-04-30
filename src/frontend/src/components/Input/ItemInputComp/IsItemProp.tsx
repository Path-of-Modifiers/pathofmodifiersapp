import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

const convertToBoolean = (value: string) => {
  if (value === "true") {
    return true;
  } else if (value === "false") {
    return false;
  } else {
    return undefined;
  }
};

const handleChange = (
  event: React.ChangeEvent<HTMLSelectElement>,
  itemSpecKey: string
) => {
  const selectedValue = convertToBoolean(event.target.value);
  switch (itemSpecKey) {
    case "identified":
      useGraphInputStore.setState({
        itemSpecState: { identified: selectedValue },
      });
      break;
    case "corrupted":
      useGraphInputStore.setState({
        itemSpecState: { corrupted: selectedValue },
      });
      break;
    case "delve":
      useGraphInputStore.setState({ itemSpecState: { delve: selectedValue } });
      break;
    case "fractured":
      useGraphInputStore.setState({
        itemSpecState: { fractured: selectedValue },
      });
      break;
    case "synthesised":
      useGraphInputStore.setState({
        itemSpecState: { synthesized: selectedValue },
      });
      break;
    case "replica":
      useGraphInputStore.setState({
        itemSpecState: { replica: selectedValue },
      });
      break;
    case "elder":
      useGraphInputStore.setState({
        itemSpecState: { influences: { elder: selectedValue } },
      });
      break;
    case "shaper":
      useGraphInputStore.setState({
        itemSpecState: { influences: { shaper: selectedValue } },
      });
      break;
    case "crusader":
      useGraphInputStore.setState({
        itemSpecState: { influences: { crusader: selectedValue } },
      });
      break;
    case "redeemer":
      useGraphInputStore.setState({
        itemSpecState: { influences: { redeemer: selectedValue } },
      });
      break;
    case "hunter":
      useGraphInputStore.setState({
        itemSpecState: { influences: { hunter: selectedValue } },
      });
      break;
    case "warlord":
      useGraphInputStore.setState({
        itemSpecState: { influences: { warlord: selectedValue } },
      });
      break;
    case "searing":
      useGraphInputStore.setState({
        itemSpecState: { searing: selectedValue },
      });
      break;
    case "tangled":
      useGraphInputStore.setState({
        itemSpecState: { tangled: selectedValue },
      });
      break;
    case "isRelic":
      useGraphInputStore.setState({
        itemSpecState: { isRelic: selectedValue },
      });
      break;
  }
};

interface IsItemInputProps {
  itemSpecKey: string;
  text: string;
}

export const IsItemInput = ({ itemSpecKey, text }: IsItemInputProps) => {
  return (
    <Flex alignItems="center" bgColor={"ui.secondary"} color={"ui.white"} m={2}>
      <Text width={150}>{text}</Text>
      <Select
        bgColor={"ui.input"}
        defaultValue={"IsItems"}
        onChange={(e) => handleChange(e, itemSpecKey)}
        width={150}
        color={"ui.white"}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={{ text } + "_IsItems"}
      >
        {
          <option
            value={undefined}
            key={text + "_IsItems_" + "undefined"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            Any
          </option>
        }
        ,
        {
          <option
            value={"true"}
            key={text + "_IsItems_" + "yes"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            Yes
          </option>
        }
        ,
        {
          <option
            value={"false"}
            key={text + "_IsItems_" + "no"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            No
          </option>
        }
      </Select>
    </Flex>
  );
};
