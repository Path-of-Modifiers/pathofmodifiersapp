import { ModifierInput } from "./ModifierInput";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { getEventTextContent } from "../../../hooks/utils";

interface TextRollInputProps {
  modifierSelected: ModifierInput;
  inputPosition: number;
}

// Text Roll Input Component  -  This component is used to select the text roll of a modifier
export const TextRollInput = ({
  modifierSelected,
  inputPosition,
}: TextRollInputProps) => {
  const { setTextRollModifierSpec } = useGraphInputStore();

  if (!modifierSelected.textRolls) {
    return null;
  }
  // Get the text rolls of the modifier at the input position
  const textRolls = modifierSelected.textRolls[inputPosition] as string;
  const textRollsList = textRolls.split("-"); // Split the text rolls into a list

  const getTextRollInput = () => {
    let textRollSelected =
      useGraphInputStore
        .getState()
        .modifierSpecs.find(
          (modifier) =>
            modifier.modifierId === modifierSelected.modifierId[inputPosition]
        )?.modifierLimitations?.textRoll ?? undefined;

    if (textRollSelected) {
      textRollSelected = textRollSelected + 1; // To account for the "Any" option
      if (textRollSelected === 0) {
        return undefined;
      } else {
        return textRollsList[textRollSelected];
      }
    }
  };

  const setGlobalStoreTextRoll = (textRoll: string) => {
    const textRollIndex = textRollsList.indexOf(textRoll);
    const modifierId = modifierSelected.modifierId[inputPosition];
    if (modifierId) {
      setTextRollModifierSpec(modifierId, textRollIndex);
    }
  };

  const defaultValue = undefined;

  // Function to handle the change of the text roll input value
  const handleTextChange = (
    event: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>
  ) => {
    const textRollInput = getEventTextContent(event);
    const textRollIndex = textRollsList.indexOf(textRollInput);
    setGlobalStoreTextRoll(textRollInput);

    if (modifierSelected.textRollInputs) {
      modifierSelected.textRollInputs[inputPosition] = textRollIndex;
    } else {
      modifierSelected.textRollInputs = [textRollIndex];
    }
  };

  // Create the text roll options
  const textRollsOptions: Array<SelectBoxOptionValue> = [
    { value: "", text: "Any" },
    ...textRollsList.map((textRoll) => {
      return {
        value: textRoll,
        text: textRoll,
      };
    }),
  ];

  return (
    <SelectBoxInput
      optionsList={textRollsOptions}
      itemKeyId={"TextRollInput"}
      defaultValue={defaultValue}
      defaultText={"Any"}
      isDimmed={!modifierSelected.isSelected}
      getSelectValue={getTextRollInput}
      handleChange={(e) => handleTextChange(e)}
    />
  );
};
