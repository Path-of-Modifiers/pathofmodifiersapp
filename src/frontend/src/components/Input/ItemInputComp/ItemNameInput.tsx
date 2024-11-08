import { useEffect } from "react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
    SelectBoxInput,
    SelectBoxOptionValue,
    HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

// Item Name Input Component  -  This component is used to input the name of an item.
export const ItemNameInput = () => {
    const { itemName, setItemName, choosableItemNames, updateChoosable } =
        useGraphInputStore();

    useEffect(() => {
        updateChoosable(itemName);
    }, [itemName, updateChoosable]);

    const handleNameChange: HandleChangeEventFunction = (newValue) => {
        if (newValue != null) {
            const itemNameText = newValue.value;
            if (itemNameText === "Any") {
                setItemName(undefined);
            } else {
                setItemName(itemNameText);
            }
        }
    };

    const optionsList: SelectBoxOptionValue[] = choosableItemNames.map(
        (itemName) => ({
            value: itemName,
            label: itemName,
            regex: itemName,
        })
    );

    return (
        <SelectBoxInput
            descriptionText="Item Name"
            optionsList={optionsList}
            defaultText={itemName !== undefined ? itemName : "Any"}
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
