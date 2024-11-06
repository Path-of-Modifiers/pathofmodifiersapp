import { useGraphInputStore } from "../../../store/GraphInputStore";
import { SetItemSpecMisc } from "../../../store/StateInterface";
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
    | "synthesised"
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
    itemSpec,
    setItemSpecIdentified,
    setItemSpecCorrupted,
    setItemSpecDelve,
    setItemSpecFractured,
    setItemSpecSynthesised,
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

  let presetValue: boolean | undefined | null;
  let setItemSpecMisc: SetItemSpecMisc;
  switch (itemSpecKey) {
    case "identified":
      presetValue = itemSpec?.identified;
      setItemSpecMisc = setItemSpecIdentified;
      break;
    case "corrupted":
      presetValue = itemSpec?.corrupted;
      setItemSpecMisc = setItemSpecCorrupted;
      break;
    case "delve":
      presetValue = itemSpec?.delve;
      setItemSpecMisc = setItemSpecDelve;
      break;
    case "fractured":
      presetValue = itemSpec?.fractured;
      setItemSpecMisc = setItemSpecFractured;
      break;
    case "synthesised":
      presetValue = itemSpec?.synthesized;
      setItemSpecMisc = setItemSpecSynthesised;
      break;
    case "replica":
      presetValue = itemSpec?.replica;
      setItemSpecMisc = setItemSpecReplica;
      break;
    case "elder":
      presetValue = itemSpec?.influences?.elder;
      setItemSpecMisc = setItemSpecElderInfluence;
      break;
    case "shaper":
      presetValue = itemSpec?.influences?.shaper;
      setItemSpecMisc = setItemSpecShaperInfluence;
      break;
    case "crusader":
      presetValue = itemSpec?.influences?.crusader;
      setItemSpecMisc = setItemSpecCrusaderInfluence;
      break;
    case "redeemer":
      presetValue = itemSpec?.influences?.redeemer;
      setItemSpecMisc = setItemSpecRedeemerInfluence;
      break;
    case "hunter":
      presetValue = itemSpec?.influences?.hunter;
      setItemSpecMisc = setItemSpecHunterInfluence;
      break;
    case "warlord":
      presetValue = itemSpec?.influences?.warlord;
      setItemSpecMisc = setItemSpecWarlordInfluence;
      break;
    case "searing":
      presetValue = itemSpec?.searing;
      setItemSpecMisc = setItemSpecSearing;
      break;
    case "tangled":
      presetValue = itemSpec?.tangled;
      setItemSpecMisc = setItemSpecTangled;
      break;
    case "isRelic":
      presetValue = itemSpec?.isRelic;
      setItemSpecMisc = setItemSpecIsRelic;
      break;
    default:
      throw "Couldn't match 'itemSpecKey' with item spec set function.";
  }

  const handleIsItemChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const textContent = newValue.value;
      const selectedValue = convertToBoolean(textContent) as boolean;
      setItemSpecMisc(selectedValue);
    }
  };

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "true", label: "Yes", regex: "Yes" },
    { value: "false", label: "No", regex: "No" },
  ];

  const defaultOption = optionsList.find(
    (option) => convertToBoolean(option.value) === presetValue
  );

  return (
    <SelectBoxInput
      descriptionText={text}
      optionsList={optionsList}
      defaultText={defaultOption ? defaultOption.label : "Any"}
      multipleValues={false}
      handleChange={handleIsItemChange}
      id={`miscItemInput-${itemSpecKey}-0`}
      canBeAny={true}
    />
  );
};
