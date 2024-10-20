import { FlexProps } from "@chakra-ui/layout";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "../StandardLayoutInput/SelectBoxInput";

type HandleTextChangeEventFunction = (value: string | undefined) => void;

export interface TextRollInputProps {
  flexProps?: FlexProps;
  textRolls: string;
  index: number;
  handleTextChange: HandleTextChangeEventFunction;
  defaultValue?: string;
  isDimmed?: boolean;
}

export const TextRollInput = (props: TextRollInputProps) => {
  const textRollArray = props.textRolls.split("|");
  const textRollOptions: SelectBoxOptionValue[] = textRollArray.map(
    (textRoll) => {
      const selectOption: SelectBoxOptionValue = {
        label: textRoll,
        value: textRoll,
        regex: textRoll,
      };
      return selectOption;
    }
  );
  return (
    <SelectBoxInput
      optionsList={textRollOptions}
      defaultText={props.defaultValue ?? "Any"}
      multipleValues={false}
      handleChange={(e) => props.handleTextChange(e?.value ?? undefined)}
      id={`TextRollInput-${props.index}`}
      isDimmed={props.isDimmed}
      flexProps={props.flexProps}
      autoFocus={true}
      canBeAny={true}
      unstyled={true}
    />
  );
};
