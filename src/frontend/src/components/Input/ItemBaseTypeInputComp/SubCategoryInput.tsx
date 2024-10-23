import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

interface SubCategoryInputProps {
  subCategories: string[];
}

// Sub Category Input Component  -  This component is used to select the sub category of an item base type.
export const SubCategoryInput = (props: SubCategoryInputProps) => {
  if (!Array.isArray(props.subCategories)) {
    props.subCategories = [props.subCategories];
  }

  const { setItemSubCategory } = useGraphInputStore();

  const handleSubCategoryChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const itemSubCategory = newValue.value;
      if (itemSubCategory === "Any") {
        setItemSubCategory(undefined);
      } else {
        setItemSubCategory(itemSubCategory);
      }
    }
  };

  const subCategoryOptions: Array<SelectBoxOptionValue> =
    props.subCategories.map((subCategory) => {
      return {
        value: subCategory,
        label: capitalizeFirstLetter(subCategory),
        regex: subCategory,
      };
    });

  return (
    <SelectBoxInput
      descriptionText={"Item Sub Category"}
      optionsList={subCategoryOptions}
      defaultText="Any"
      multipleValues={false}
      handleChange={handleSubCategoryChange}
      id={"subcategoryInput-0"}
      canBeAny={true}
    />
  );
};
