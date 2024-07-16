import { useGraphInputStore } from "../../../store/GraphInputStore";
import { capitalizeFirstLetter } from "../../../hooks/utils";
import { ItemBaseTypeSubCategory } from "../../../client";
import { SelectBox, SelectBoxOptionValue } from "../StandardLayoutInput/SelectBoxInput";

interface SubCategoryInputProps {
  subCategories: ItemBaseTypeSubCategory | ItemBaseTypeSubCategory[];
}

// Sub Category Input Component  -  This component is used to select the sub category of an item base type.
export const SubCategoryInput = ({ subCategories }: SubCategoryInputProps) => {
  if (!Array.isArray(subCategories)) {
    subCategories = [subCategories];
  }

  const defaultValue = undefined;

  const getSubCategoryValue = () => {
    const baseType = useGraphInputStore.getState().baseSpec?.subCategory;
    if (baseType) {
      return baseType;
    } else {
      return "";
    }
  };

  const { setItemSubCategory } = useGraphInputStore();

  const handleSubCategoryChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const itemSubCategory = event.target.value;
    if (itemSubCategory === "Any") {
      setItemSubCategory(undefined);
    }
    setItemSubCategory(itemSubCategory);
  };

  const subCategoryOptions: Array<SelectBoxOptionValue> = subCategories.map((subCategory) => {
    return {
      value: subCategory.subCategory,
      text: capitalizeFirstLetter(subCategory.subCategory),
    };
  });

  return (
    <SelectBox
      descriptionText={"Item Sub Category"}
      optionsList={subCategoryOptions}
      itemKeyId={"ItemSubCategoryInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectValue={getSubCategoryValue}
      handleChange={(e) => handleSubCategoryChange(e)}
    />
  );
};
