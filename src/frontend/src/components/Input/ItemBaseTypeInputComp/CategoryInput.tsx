import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import { ItemBaseTypeCategory } from "../../../client";
import {
  SelectBox,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBox";

interface CategoryInputProps {
  categories: ItemBaseTypeCategory | ItemBaseTypeCategory[];
}

// Category Input Component  -  This component is used to select the category of an item base type.
export const CategoryInput = ({ categories }: CategoryInputProps) => {
  if (!Array.isArray(categories)) {
    categories = [categories];
  }

  const defaultValue = undefined;

  const { setItemCategory } = useGraphInputStore();

  const getCategoryValue = () => {
    const category = useGraphInputStore.getState().baseSpec?.category;
    if (category) {
      return category;
    } else {
      return "";
    }
  };

  const handleCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const itemCategory = event.target.value;
    if (itemCategory === "Any") {
      setItemCategory(undefined);
    }
    setItemCategory(itemCategory);
  };

  const categoryOptions: Array<SelectBoxOptionValue> = categories.map(
    (baseCategory) => {
      return {
        value: baseCategory.category,
        text: capitalizeFirstLetter(baseCategory.category),
      };
    }
  );

  return (
    <SelectBox
      descriptionText={"Item Category"}
      optionsList={categoryOptions}
      itemKeyId={"ItemCategoryInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectValue={getCategoryValue}
      handleChange={(e) => handleCategoryChange(e)}
    />
  );
};
