import {
  GetValueFunction,
  HandleChangeEventFunction,
} from "../../../schemas/function/InputFunction";
import { SelectBoxInput, SelectBoxOptionValue } from "./SelectBoxInput";

interface TextInputProps {
  getTextValue: GetValueFunction;
  handleTextChange: HandleChangeEventFunction;
}

// Item Name Input Component  -  This component is used to input the name of an item.
export const TextInput = ({
  getTextValue,
  handleTextChange,
}: TextInputProps) => {
  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "", text: "Any" },
    { value: "Grand Spectrum", text: "Grand Spectrum" },
    { value: "Forbidden Flesh", text: "Forbidden Flesh" },
    { value: "The Balance of Terror", text: "The Balance of Terror" },
    { value: "That Which Was Taken", text: "That Which Was Taken" },
    { value: "Forbidden Flame", text: "Forbidden Flame" },
    { value: "Split Personality", text: "Split Personality" },
    { value: "Thread of Hope", text: "Thread of Hope" },
    { value: "Impossible Escape", text: "Impossible Escape" },
    { value: "Watcher's Eye", text: "Watcher's Eye" },
    { value: "Sublime Vision", text: "Sublime Vision" },
    { value: "Glorious Vanity", text: "Glorious Vanity" },
    { value: "Lethal Pride", text: "Lethal Pride" },
    { value: "Brutal Restraint", text: "Brutal Restraint" },
    { value: "Militant Faith", text: "Militant Faith" },
    { value: "Elegant Hubris", text: "Elegant Hubris" },
    { value: "Voices", text: "Voices" },
  ];

  return (
    <SelectBoxInput
      descriptionText="Item Name"
      optionsList={optionsList}
      itemKeyId="itemName"
      defaultText="Any"
      defaultValue={undefined}
      getSelectValue={getTextValue}
      handleChange={handleTextChange}
    />
  );
};
