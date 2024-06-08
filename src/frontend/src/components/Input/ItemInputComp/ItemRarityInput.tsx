import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  SelectBox,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBox";

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

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const itemRarityInput = event.target.value;
    if (itemRarityInput === "Any") {
      setItemRarity(undefined);
    } else {
      setItemRarity(itemRarityInput);
    }
  };

  const optionsList: Array<SelectBoxOptionValue> = [
    { value: "Unique", text: "Unique" },
    /* Future implementation for non-unique items
    { value: "Non_Unique", text: "Any Non-Unique" },
    */
  ];

  return (
    <SelectBox
      descriptionText={"Item Rarity"}
      optionsList={optionsList}
      itemKeyId={"ItemRarityInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectValue={getRarityValue}
      handleChange={(e) => handleChange(e)}
    ></SelectBox>
  );
};
