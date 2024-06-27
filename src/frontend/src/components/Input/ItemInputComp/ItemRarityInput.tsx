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

  const getRarityTextValue = () => {
    const rarity = useGraphInputStore.getState().itemSpec.rarity;
    if (rarity) {
      return rarity;
    } else {
      return "";
    }
  };

  const handleItemRarityChange = (
    event: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>
  ) => {
    const itemRarityInput = getEventTextContent(event);
    if (itemRarityInput === "Any") {
      setItemRarity(undefined);
    } else {
      setItemRarity(itemRarityInput);
    }
  };

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: undefined, text: "Any" },
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
      getSelectTextValue={getRarityTextValue()}
      handleChange={(e) => handleItemRarityChange(e)}
    />
  );
};
