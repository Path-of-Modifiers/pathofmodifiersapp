import {
  ItemNameInput,
  ItemNameInputProps,
} from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";

interface ItemInputProps {
  itemNameInputProps: ItemNameInputProps;
}

// Item Input Component  -  This component is used to input item name and rarity
export const ItemInput = (props: ItemInputProps) => {
  return (
    <>
      <ItemNameInput {...props.itemNameInputProps} />
      <ItemRarityInput />
    </>
  );
};
