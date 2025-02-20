import { ItemNameInput } from "./ItemInputComp/ItemNameInput";
import { ItemRarityInput } from "./ItemInputComp/ItemRarityInput";

// Item Input Component  -  This component is used to input item name and rarity
export const ItemInput = () => {
    return (
        <>
            <ItemNameInput />
            <ItemRarityInput />
        </>
    );
};
