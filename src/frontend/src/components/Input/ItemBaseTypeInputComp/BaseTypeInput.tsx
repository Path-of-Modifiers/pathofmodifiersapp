import { useGraphInputStore } from "../../../store/GraphInputStore";
import { BaseType } from "../../../client";
import {
  SelectBox,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";

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
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const baseType = event.target.value;
    if (baseType === "Any") {
      setBaseType(undefined);
    }
    setBaseType(baseType);
  };

  const baseTypeOptions: Array<SelectBoxOptionValue> = baseTypes.map(
    (baseType) => {
      return {
        value: baseType.baseType,
        text: baseType.baseType,
      };
    }
  );

  return (
    <SelectBox
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
