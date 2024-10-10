import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

// Item Rarity Input Component  -  This component is used to select the rarity of an item.
export const ItemRarityInput = () => {
  const { setItemRarity } = useGraphInputStore();

  const handleItemRarityChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const itemRarityInput = newValue.value;
      if (itemRarityInput === "Any") {
        setItemRarity(undefined);
      } else {
        setItemRarity(itemRarityInput);
      }
    }
  };

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "Unique", label: "Unique", regex: "Unique" },
    /* Future implementation for non-unique items
    { value: "Non_Unique", label: "Any Non-Unique" },
    */
  ];

  return (
    <SelectBoxInput
      descriptionText={"Item Rarity"}
      optionsList={optionsList}
      defaultText="Any"
      multipleValues={false}
      handleChange={handleItemRarityChange}
      id={"itemRarityInput-0"}
      canBeAny={true}
    />
  );
};
