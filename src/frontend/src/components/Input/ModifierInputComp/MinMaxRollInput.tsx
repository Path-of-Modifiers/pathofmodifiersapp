import { SelectedModifier } from "./ModifierInput";
import { MinMaxNumberInput } from "../StandardLayoutInput/MinMaxNumberInput";
import { useGraphInputStore } from "../../../store/GraphInputStore";

interface MinRollInputProps {
  modifierSelected: SelectedModifier;
  inputPosition: number;
}

// Min Roll Input Component  -  This component is used to input the minimum roll of a modifier
export const MinMaxRollInput = ({
  modifierSelected,
  inputPosition,
}: MinRollInputProps) => {
  const minSpecKey = (
    "min_" +
    modifierSelected.modifierId[0] +
    inputPosition
  ).toString();
  const maxSpecKey = (
    "max_" +
    modifierSelected.modifierId[0] +
    inputPosition
  ).toString();

  const { setMinRollModifierSpec, setMaxRollModifierSpec } =
    useGraphInputStore();

  if (!modifierSelected.minRoll) {
    return null;
  }

  const getGlobalMinValue = () => {
    const globalModifierSelectedMinRoll =
      useGraphInputStore
        .getState()
        .modifierSpecs.find(
          (modifier) =>
            modifier.modifierId === modifierSelected.modifierId[inputPosition]
        )?.modifierLimitations?.minRoll ?? undefined;

    return globalModifierSelectedMinRoll ?? "";
  };

  const getGlobalMaxValue = () => {
    const globalModifierSelectedMaxRoll =
      useGraphInputStore
        .getState()
        .modifierSpecs.find(
          (modifier) =>
            modifier.modifierId === modifierSelected.modifierId[inputPosition]
        )?.modifierLimitations?.maxRoll ?? undefined;

    return globalModifierSelectedMaxRoll ?? "";
  };

  const setGlobalStoreMinRoll = (minRoll: number) => {
    const modifierId = modifierSelected.modifierId[inputPosition];
    if (modifierId) {
      setMinRollModifierSpec(modifierId, minRoll);
    }
  };

  const setGlobalStoreMaxRoll = (maxRoll: number) => {
    const modifierId = modifierSelected.modifierId[inputPosition];
    if (modifierId) {
      setMaxRollModifierSpec(modifierId, maxRoll);
    }
  };

  // Function to handle the change of the min roll input value
  const handleMinChange = (eventValue: string) => {
    const eventFloatValue = parseFloat(eventValue);
    // If the min roll input is defined, set the value of the input at the input position to the event value
    if (modifierSelected.minRollInputs) {
      modifierSelected.minRollInputs[inputPosition] = eventFloatValue;
      setGlobalStoreMinRoll(eventFloatValue);
    } else {
      modifierSelected.minRollInputs = [eventFloatValue];
      setGlobalStoreMinRoll(eventFloatValue);
    }
  };

  // Function to handle the change of the max roll input value
  const handleMaxChange = (eventValue: string) => {
    const eventFloatValue = parseFloat(eventValue);
    // If the max roll input is defined, set the value of the input at the input position to the event value
    if (modifierSelected.maxRollInputs) {
      modifierSelected.maxRollInputs[inputPosition] = parseFloat(eventValue);
      setGlobalStoreMaxRoll(eventFloatValue);
    } else {
      modifierSelected.maxRollInputs = [parseFloat(eventValue)];
      setGlobalStoreMaxRoll(eventFloatValue);
    }
  };

  return (
    <MinMaxNumberInput
      minSpecKey={minSpecKey}
      maxSpecKey={maxSpecKey}
      isDimmed={!modifierSelected.isSelected}
      getMinValue={getGlobalMinValue}
      getMaxValue={getGlobalMaxValue}
      handleMinChange={handleMinChange}
      handleMaxChange={handleMaxChange}
    />
  );
};
