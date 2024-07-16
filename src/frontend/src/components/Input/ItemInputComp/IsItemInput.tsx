import { useGraphInputStore } from "../../../store/GraphInputStore";
import { convertToBoolean } from "../../../hooks/utils";
import { ItemSpecState } from "../../../store/StateInterface";
import { SelectBox, SelectBoxOptionValue } from "../StandardLayoutInput/SelectBoxInput";

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

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
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

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "true", text: "Yes" },
    { value: "false", text: "No" },
  ];

  return (
    <SelectBox
      descriptionText={text}
      optionsList={optionsList}
      itemKeyId={itemSpecKey}
      defaultValue={undefined}
      defaultText="Any"
      getSelectValue={getSelectValue}
      handleChange={(e) => handleChange(e)}
    ></SelectBox>
  );
};
