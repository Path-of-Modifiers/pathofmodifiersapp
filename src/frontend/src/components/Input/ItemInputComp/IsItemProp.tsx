import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { convertToBoolean } from "../../../hooks/utils";
import { ItemSpecState } from "../../../store/StateInterface";

interface IsItemInputProps {
  itemSpecKey:
    | "identified"
    | "corrupted"
    | "delve"
    | "fractured"
    | "synthesized"
    | "replica"
    | "elder"
    | "shaper"
    | "crusader"
    | "redeemer"
    | "hunter"
    | "warlord"
    | "searing"
    | "tangled"
    | "isRelic";
  text: string;
}

// Is Item Input Component  -  This component is used to select the boolean item properties.
export const IsItemInput = ({ itemSpecKey, text }: IsItemInputProps) => {
  const defaultValue = undefined;

  const getSelectValue = () => {
    let selectValue = undefined;
    if (
      itemSpecKey === "elder" ||
      itemSpecKey === "shaper" ||
      itemSpecKey === "crusader" ||
      itemSpecKey === "redeemer" ||
      itemSpecKey === "hunter" ||
      itemSpecKey === "warlord"
    ) {
      selectValue =
        (useGraphInputStore.getState().itemSpec as ItemSpecState).influences?.[
          itemSpecKey
        ] ?? undefined;
    } else {
      selectValue = (useGraphInputStore.getState().itemSpec as ItemSpecState)[
        itemSpecKey
      ];
    }
    if (selectValue) {
      return "true";
    } else if (selectValue === false) {
      return "false";
    }
    return "";
  };

  const {
    setItemSpecIdentified,
    setItemSpecCorrupted,
    setItemSpecDelve,
    setItemSpecFractured,
    setItemSpecSynthesized,
    setItemSpecReplica,
    setItemSpecElderInfluence,
    setItemSpecShaperInfluence,
    setItemSpecCrusaderInfluence,
    setItemSpecRedeemerInfluence,
    setItemSpecHunterInfluence,
    setItemSpecWarlordInfluence,
    setItemSpecSearing,
    setItemSpecTangled,
    setItemSpecIsRelic,
  } = useGraphInputStore();

  const handleChange = (
    event: React.ChangeEvent<HTMLSelectElement>,
    itemSpecKey: string
  ) => {
    const selectedValue = convertToBoolean(event.target.value) as boolean;

    switch (itemSpecKey) {
      case "identified":
        setItemSpecIdentified(selectedValue);
        break;
      case "corrupted":
        setItemSpecCorrupted(selectedValue);
        break;
      case "delve":
        setItemSpecDelve(selectedValue);
        break;
      case "fractured":
        setItemSpecFractured(selectedValue);
        break;
      case "synthesized":
        setItemSpecSynthesized(selectedValue);
        break;
      case "replica":
        setItemSpecReplica(selectedValue);
        break;
      case "elder":
        setItemSpecElderInfluence(selectedValue);
        break;
      case "shaper":
        setItemSpecShaperInfluence(selectedValue);
        break;
      case "crusader":
        setItemSpecCrusaderInfluence(selectedValue);
        break;
      case "redeemer":
        setItemSpecRedeemerInfluence(selectedValue);
        break;
      case "hunter":
        setItemSpecHunterInfluence(selectedValue);
        break;
      case "warlord":
        setItemSpecWarlordInfluence(selectedValue);
        break;
      case "searing":
        setItemSpecSearing(selectedValue);
        break;
      case "tangled":
        setItemSpecTangled(selectedValue);
        break;
      case "isRelic":
        setItemSpecIsRelic(selectedValue);
        break;
    }
  };

  return (
    <Flex alignItems="center" bgColor={"ui.secondary"} color={"ui.white"} m={1}>
      <Text ml={1} width={150}>
        {text}
      </Text>
      <Select
        value={getSelectValue()}
        bgColor={"ui.input"}
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
            value={defaultValue}
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
