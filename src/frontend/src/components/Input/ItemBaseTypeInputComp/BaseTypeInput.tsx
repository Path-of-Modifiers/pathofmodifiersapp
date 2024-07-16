import { useGraphInputStore } from "../../../store/GraphInputStore";
import { BaseType } from "../../../client";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";
import { getEventTextContent } from "../../../hooks/utils";

interface BaseTypeInputProps {
  baseTypes: BaseType | BaseType[];
}

// Base Type Input Component  -  This component is used to select the base type of an item.
export const BaseTypeInput = (props: BaseTypeInputProps) => {
  if (!Array.isArray(props.baseTypes)) {
    props.baseTypes = [props.baseTypes];
  }

  const defaultValue = undefined;

  const { setBaseType } = useGraphInputStore();

  const getBaseTypeValue = () => {
    const baseType = useGraphInputStore.getState().baseSpec?.baseType;
    if (baseType) {
      return baseType;
    } else {
      return "";
    }
  };

  const handleBaseTypeChange = (
    event: React.FormEvent<HTMLElement> | React.MouseEvent<HTMLElement>
  ) => {
    const baseType = getEventTextContent(event);
    if (baseType === "Any") {
      setBaseType(undefined);
    } else {
      setBaseType(baseType);
    }
  };

  const baseTypeOptions: Array<SelectBoxOptionValue> = [
    { value: "", text: "Any" },
    ...props.baseTypes.map((baseType) => {
      return {
        value: baseType.baseType,
        text: baseType.baseType,
      };
    }),
  ];

  return (
    <SelectBoxInput
      descriptionText={"Item Base Type"}
      optionsList={baseTypeOptions}
      itemKeyId={"BaseTypeInput"}
      defaultValue={defaultValue}
      defaultText="Any"
      getSelectTextValue={getBaseTypeValue()}
      handleChange={(e) => handleBaseTypeChange(e)}
    />
  );
};
