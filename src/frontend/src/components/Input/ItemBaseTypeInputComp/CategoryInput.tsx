import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  capitalizeFirstLetter,
  getEventTextContent,
} from "../../../hooks/utils";
import { ItemBaseTypeCategory } from "../../../client";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";

interface CategoryInputProps {
  categories: ItemBaseTypeCategory | ItemBaseTypeCategory[];
}

// Category Input Component  -  This component is used to select the category of an item base type.
export const CategoryInput = (props: CategoryInputProps) => {
  if (!Array.isArray(props.categories)) {
    props.categories = [props.categories];
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
    event: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>
  ) => {
    const itemCategory = getEventTextContent(event);
    if (itemCategory === "Any") {
      setItemCategory(undefined);
    } else {
      setItemCategory(itemCategory);
    }
  };

  const categoryOptions: Array<SelectBoxOptionValue> = [
    { value: "", text: "Any" },
    ...props.categories.map((baseCategory) => {
      return {
        value: baseCategory.category,
        text: capitalizeFirstLetter(baseCategory.category),
      };
    }),
  ];

  return (
    <SelectBoxInput
      descriptionText={"Item Category"}
      optionsList={categoryOptions}
      itemKeyId={"ItemCategoryInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectTextValue={getCategoryValue()}
      handleChange={(e) => handleCategoryChange(e)}
    />
  );
};
