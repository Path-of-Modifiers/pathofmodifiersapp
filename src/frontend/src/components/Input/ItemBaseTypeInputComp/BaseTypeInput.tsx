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
export const BaseTypeInput = ({ baseTypes }: BaseTypeInputProps) => {
  if (!Array.isArray(baseTypes)) {
    baseTypes = [baseTypes];
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
    event: React.FormEvent<HTMLElement> | React.ChangeEvent<HTMLInputElement>
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
    ...baseTypes.map((baseType) => {
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
      getSelectValue={getBaseTypeValue}
      handleChange={(e) => handleBaseTypeChange(e)}
    />
  );
};
