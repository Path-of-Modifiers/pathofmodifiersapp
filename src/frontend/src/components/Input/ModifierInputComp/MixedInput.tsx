import { useGraphInputStore } from "../../../store/GraphInputStore";
import { MinMaxNumberInput } from "../StandardLayoutInput/MinMaxNumberInput";
import { TextRollInput } from "./TextRollInput";
import { ModifierOption } from "./ModifierInput";
import { HStack } from "@chakra-ui/layout";

export interface MixedInputProps {
  selectedModifier: ModifierOption;
  index: number;
  isDimmed?: boolean;
  nPossibleInputs: number;
  ml: string;
}

export type HandleChangeEventFunction = (
  isNumerical: boolean,
  modifierId: number,
  value: string | undefined,
  index_to_handle: number,
  numericalType?: string,
  textRolls?: string
) => void;

export const MixedInput = (props: MixedInputProps) => {
  const isStatic = props.selectedModifier.static === null;
  const {
    setWantedModifierMinRoll,
    setWantedModifierMaxRoll,
    setWantedModifierTextRoll,
  } = useGraphInputStore();
  if (isStatic) {
    return;
  }

  const handleAnyChange: HandleChangeEventFunction = (
    isNumerical: boolean,
    modifierId: number,
    value: string | undefined,
    index_to_handle: number,
    numericalType?: string,
    textRolls?: string
  ): void => {
    if (isNumerical && numericalType !== undefined) {
      const numValue = value !== undefined ? Number(value) : undefined;
      if (numericalType === "min") {
        setWantedModifierMinRoll(modifierId, numValue, index_to_handle);
      } else if (numericalType === "max") {
        setWantedModifierMaxRoll(modifierId, numValue, index_to_handle);
      } else {
        throw `numerical type needs to be 'min' or 'max', not ${numericalType}`;
      }
    } else if (isNumerical && numericalType === undefined) {
      throw "Numerical type must be specified if 'isNumerical`===true";
    } else if (!isNumerical && textRolls) {
      if (value === "Any") {
        value = undefined;
      }
      const textValue =
        value !== undefined ? textRolls.split("|").indexOf(value) : undefined;
      setWantedModifierTextRoll(modifierId, textValue, index_to_handle);
    } else {
      throw "Modifier must have text rolls if the roll is not numerical.";
    }
  };
  const mixedInput = props.selectedModifier.groupedModifier.modifierId.map(
    (modifierId, index) => {
      const textRolls = props.selectedModifier.groupedModifier.textRolls[index];
      const isNumerical = textRolls === null;
      if (isNumerical) {
        return (
          <MinMaxNumberInput
            isDimmed={props.isDimmed}
            index={props.index}
            handleNumberChange={(value: string, numericalType: string) =>
              handleAnyChange(
                isNumerical,
                modifierId,
                value,
                props.index,
                numericalType
              )
            }
            key={`min-max-input-${props.index}-${index}`}
            flexProps={{
              w: `${Math.floor(100 / props.nPossibleInputs) - 1}%`,
              h: 10,
            }}
            numberInputProps={{ h: 5 }}
          />
        );
      } else {
        return (
          <TextRollInput
            textRolls={textRolls ?? ""}
            index={props.index}
            handleTextChange={(value) =>
              handleAnyChange(
                isNumerical,
                modifierId,
                value,
                props.index,
                undefined,
                textRolls
              )
            }
            isDimmed={props.isDimmed}
            key={`text-input-${props.index}-${index}`}
            flexProps={{
              w: `${Math.floor(100 / props.nPossibleInputs) - 1}%`,
              h: 10,
            }}
          />
        );
      }
    }
  );
  return (
    // justify="right"
    // w="45%"
    // w={props.w}
    <HStack w="100%" h={10}>
      {mixedInput}
    </HStack>
  );
};
