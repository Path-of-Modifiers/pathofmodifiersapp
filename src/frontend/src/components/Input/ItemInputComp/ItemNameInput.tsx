import { useGraphInputStore } from "../../../store/GraphInputStore";
import { TextInput } from "../StandardLayoutInput/TextInput";

// Item Name Input Component  -  This component is used to input the name of an item.
export const ItemNameInput = () => {
  const { setItemName } = useGraphInputStore();

  const getItemNameValue = () => {
    const itemName = useGraphInputStore.getState().itemSpec.name;
    if (itemName) {
      return itemName;
    } else {
      return "";
    }
  };

  const handleNameChange = (value: string) => {
    const itemNameInput = value;
    setItemName(itemNameInput);
  };

  return (
    <TextInput
      getTextValue={getItemNameValue}
      handleTextChange={handleNameChange}
    />
  );
};
