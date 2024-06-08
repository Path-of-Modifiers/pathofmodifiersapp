import { useGraphInputStore } from "../../../store/GraphInputStore";
import { MinMaxNumberInput } from "../StandardLayoutInput/MinMaxNumberInput";

interface MinMaxInputProps {
  itemMinSpecKey: string;
  itemMaxSpecKey: string;
  text: string;
}

// Min Max Item Lvl Input Component  -  This component is used to input the min and max ilvl of an item.
export const MinMaxInput = ({
  itemMinSpecKey,
  itemMaxSpecKey,
  text,
}: MinMaxInputProps) => {
  const { setItemSpecMinIlvl, setItemSpecMaxIlvl } = useGraphInputStore();

  const [minValue, maxValue] = useGraphInputStore((state) => [
    state.itemSpec.minIlvl,
    state.itemSpec.maxIlvl,
  ]);

  const getMinValue = () => {
    if (minValue) {
      return minValue?.toString();
    } else {
      return "";
    }
  };

  const getMaxValue = () => {
    if (maxValue) {
      return maxValue?.toString();
    } else {
      return "";
    }
  };

  const handleMinChange = (eventValue: string) => {
    const eventValueInt = parseInt(eventValue);

    setItemSpecMinIlvl(eventValueInt);
  };

  const handleMaxChange = (eventValue: string) => {
    const eventValueInt = parseInt(eventValue);

    setItemSpecMaxIlvl(eventValueInt);
  };

  return (
    <MinMaxNumberInput
      text={text}
      minSpecKey={itemMinSpecKey}
      maxSpecKey={itemMaxSpecKey}
      getMinValue={getMinValue}
      getMaxValue={getMaxValue}
      handleMinChange={handleMinChange}
      handleMaxChange={handleMaxChange}
    />
  );
};
