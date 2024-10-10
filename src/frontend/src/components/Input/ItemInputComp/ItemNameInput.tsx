import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

export interface ItemNameInputProps {
  uniques: string[];
}

// Item Name Input Component  -  This component is used to input the name of an item.
export const ItemNameInput = (props: ItemNameInputProps) => {
  const { setItemName } = useGraphInputStore();

  const handleNameChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const itemNameText = newValue.value;
      setItemName(itemNameText);
    }
  };

  const optionsList: SelectBoxOptionValue[] = props.uniques.map((unique) => ({
    value: unique,
    label: unique,
    regex: unique,
  }));

  return (
    <SelectBoxInput
      descriptionText="Item Name"
      optionsList={optionsList}
      defaultText="Any"
      multipleValues={false}
      handleChange={handleNameChange}
      flexProps={{
        width: "inputSizes.ultraPBox",
      }}
      id="itemNameInput-1"
      canBeAny={true}
    />
  );
};
