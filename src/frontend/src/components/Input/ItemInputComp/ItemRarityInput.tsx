import { getEventTextContent } from "../../../hooks/utils";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";

// Item Rarity Input Component  -  This component is used to select the rarity of an item.
export const ItemRarityInput = () => {
  const { setItemRarity } = useGraphInputStore();

  const defaultValue = undefined;

  const getRarityValue = () => {
    const rarity = useGraphInputStore.getState().itemSpec.rarity;
    if (rarity) {
      return rarity;
    } else {
      return "";
    }
  };

  const handleItemRarityChange = (
    event: React.FormEvent<HTMLElement> | React.ChangeEvent<HTMLInputElement>
  ) => {
    const itemRarityInput = getEventTextContent(event);
    if (itemRarityInput === "Any") {
      setItemRarity(undefined);
    } else {
      setItemRarity(itemRarityInput || undefined);
    }
  };

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "", text: "Any"},
    { value: "Unique", text: "Unique" },
    /* Future implementation for non-unique items
    { value: "Non_Unique", text: "Any Non-Unique" },
    */
  ];

  return (
    <SelectBoxInput
      descriptionText={"Item Rarity"}
      optionsList={optionsList}
      itemKeyId={"ItemRarityInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectValue={getRarityValue}
      handleChange={(e) => handleItemRarityChange(e)}
    />
  );
};
