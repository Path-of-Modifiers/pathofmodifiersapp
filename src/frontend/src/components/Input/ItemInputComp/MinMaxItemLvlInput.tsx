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

  const getGlobalMinValue = () => {
    const globalMin = useGraphInputStore.getState().itemSpec.minIlvl;
    return globalMin ?? "";
  };

  const getGlobalMaxValue = () => {
    const globalMax = useGraphInputStore.getState().itemSpec.maxIlvl;
    return globalMax ?? "";
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
      descriptionText={text}
      minSpecKey={itemMinSpecKey}
      maxSpecKey={itemMaxSpecKey}
      getMinValue={getGlobalMinValue}
      getMaxValue={getGlobalMaxValue}
      handleMinChange={handleMinChange}
      handleMaxChange={handleMaxChange}
    />
  );
};
