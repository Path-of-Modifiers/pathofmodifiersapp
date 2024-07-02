import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";

// Miscellaneous Item Input Component  -  This component is used to input miscellaneous item properties.
export const ItemInput = () => {
  return (
    <>
      <ItemNameInput />
      <ItemRarityInput />
    </>
  );
};
