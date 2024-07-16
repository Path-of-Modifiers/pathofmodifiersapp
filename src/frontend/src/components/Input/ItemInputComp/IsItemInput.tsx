import { useGraphInputStore } from "../../../store/GraphInputStore";
import { convertToBoolean, getEventTextContent } from "../../../hooks/utils";
import { ItemSpecState } from "../../../store/StateInterface";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";

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

  const getIsItemSelectValue = () => {
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
      return "Yes";
    } else if (selectValue === false) {
      return "No";
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

  const handleIsItemChange = (
    event: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>,
    value: string
  ) => {
    const textContent = getEventTextContent(event);
    const selectedValue = convertToBoolean(textContent) as boolean;

    switch (value) {
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

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: undefined, text: "Any" },
    { value: "true", text: "Yes" },
    { value: "false", text: "No" },
  ];

  return (
    <SelectBoxInput
      descriptionText={text}
      optionsList={optionsList}
      itemKeyId={itemSpecKey}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectTextValue={getIsItemSelectValue()}
      handleChange={(e) => handleIsItemChange(e, itemSpecKey)}
    />
  );
};
