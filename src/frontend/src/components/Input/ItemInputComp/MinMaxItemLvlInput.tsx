import { useGraphInputStore } from "../../../store/GraphInputStore";
import {
  MinMaxNumberInput,
  HandleNumberChangeEventFunction,
  DefaultMinMaxValues,
} from "../StandardLayoutInput/MinMaxNumberInput";

interface MinMaxInputProps {
  text: string;
}

// Min Max Item Lvl Input Component  -  This component is used to input the min and max ilvl of an item.
export const MinMaxIlvlInput = (props: MinMaxInputProps) => {
  const { itemSpec, setItemSpecMinIlvl, setItemSpecMaxIlvl } =
    useGraphInputStore();

  const handleMinChange = (eventValue: string) => {
    const eventValueInt = parseInt(eventValue);

    setItemSpecMinIlvl(eventValueInt);
  };

  const handleMaxChange = (eventValue: string) => {
    const eventValueInt = parseInt(eventValue);

    setItemSpecMaxIlvl(eventValueInt);
  };

  const handleNumberChange: HandleNumberChangeEventFunction = (
    value,
    numericalType
  ) => {
    if (numericalType === "min") {
      handleMinChange(value);
    } else if (numericalType === "max") {
      handleMaxChange(value);
    } else {
      throw "'numericalType' must be 'min' or 'max'";
    }
  };

  const presetValue: DefaultMinMaxValues = {
    min: itemSpec.minIlvl != null ? itemSpec.minIlvl : undefined,
    max: itemSpec.maxIlvl != null ? itemSpec.maxIlvl : undefined,
  };

  return (
    <MinMaxNumberInput
      descriptionText={props.text}
      handleNumberChange={handleNumberChange}
      defaultValues={presetValue}
    />
  );
};
