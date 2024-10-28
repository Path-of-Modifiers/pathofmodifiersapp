import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

interface CategoryInputProps {
  categories: string[];
  presetValue: string | undefined;
}

// Category Input Component  -  This component is used to select the category of an item base type.
export const CategoryInput = (props: CategoryInputProps) => {
  const { setItemCategory } = useGraphInputStore();

  const handleCategoryChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const itemCategory = newValue.value;
      if (itemCategory === "Any") {
        setItemCategory(undefined);
      } else {
        setItemCategory(itemCategory);
      }
    }
  };

  const categoryOptions: Array<SelectBoxOptionValue> = props.categories.map(
    (category) => {
      return {
        value: category,
        label: capitalizeFirstLetter(category),
        regex: category,
      };
    }
  );

  return (
    <SelectBoxInput
      descriptionText={"Item Category"}
      optionsList={categoryOptions}
      defaultText={
        props.presetValue ? capitalizeFirstLetter(props.presetValue) : "Any"
      }
      multipleValues={false}
      handleChange={handleCategoryChange}
      id={"categoryInput-0"}
      canBeAny={true}
    />
  );
};
