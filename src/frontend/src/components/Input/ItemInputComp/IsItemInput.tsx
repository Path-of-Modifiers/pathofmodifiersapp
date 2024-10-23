import { useGraphInputStore } from "../../../store/GraphInputStore";
import { convertToBoolean } from "../../../hooks/utils";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
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

  const handleIsItemChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const textContent = newValue.value;
      const selectedValue = convertToBoolean(textContent) as boolean;

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
    }
  };

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "true", label: "Yes", regex: "Yes" },
    { value: "false", label: "No", regex: "No" },
  ];

  return (
    <SelectBoxInput
      descriptionText={text}
      optionsList={optionsList}
      defaultText="Any"
      multipleValues={false}
      handleChange={handleIsItemChange}
      id={`miscItemInput-${itemSpecKey}-0`}
      canBeAny={true}
    />
  );
};
