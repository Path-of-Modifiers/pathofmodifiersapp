import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  capitalizeFirstLetter,
  getEventTextContent,
} from "../../../hooks/utils";
import { ItemBaseTypeSubCategory } from "../../../client";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";

interface SubCategoryInputProps {
  subCategories: ItemBaseTypeSubCategory | ItemBaseTypeSubCategory[];
}

// Sub Category Input Component  -  This component is used to select the sub category of an item base type.
export const SubCategoryInput = (props: SubCategoryInputProps) => {
  if (!Array.isArray(props.subCategories)) {
    props.subCategories = [props.subCategories];
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
    event: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>
  ) => {
    const itemSubCategory = getEventTextContent(event);
    if (itemSubCategory === "Any") {
      setItemSubCategory(undefined);
    } else {
      setItemSubCategory(itemSubCategory);
    }
  };

  const subCategoryOptions: Array<SelectBoxOptionValue> = [
    { value: "", text: "Any" },
    ...props.subCategories.map((subCategory) => {
      return {
        value: subCategory.subCategory,
        text: capitalizeFirstLetter(subCategory.subCategory),
      };
    }),
  ];

  return (
    <SelectBoxInput
      descriptionText={"Item Sub Category"}
      optionsList={subCategoryOptions}
      itemKeyId={"ItemSubCategoryInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectTextValue={getSubCategoryValue()}
      handleChange={(e) => handleSubCategoryChange(e)}
    />
  );
};
