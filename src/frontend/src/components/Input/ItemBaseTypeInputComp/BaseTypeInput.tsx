import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "../StandardLayoutInput/SelectBoxInput";

interface BaseTypeInputProps {
  baseTypes: string[];
}

// Base Type Input Component  -  This component is used to select the base type of an item.
export const BaseTypeInput = (props: BaseTypeInputProps) => {
  const { setBaseType } = useGraphInputStore();

  const handleBaseTypeChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      const baseType = newValue?.value;
      if (baseType === "Any") {
        setBaseType(undefined);
      } else {
        setBaseType(baseType);
      }
    }
  };

  const baseTypeOptions: Array<SelectBoxOptionValue> = props.baseTypes.map(
    (baseType) => {
      return {
        value: baseType,
        label: baseType,
        regex: baseType,
      };
    }
  );

  return (
    <SelectBoxInput
      descriptionText={"Item Base Type"}
      optionsList={baseTypeOptions}
      defaultText="Any"
      multipleValues={false}
      handleChange={handleBaseTypeChange}
      id={"baseTypeInput-0"}
      canBeAny={true}
    />
  );
};
