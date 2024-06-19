import { Flex } from "@chakra-ui/layout";
import {
  GetValueFunction,
  HandleChangeEventFunction,
} from "../../../schemas/function/InputFunction";
import {
  AutoComplete,
  AutoCompleteInput,
  AutoCompleteItem,
  AutoCompleteList,
} from "@choc-ui/chakra-autocomplete";
import { FormControl, FormLabel } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { useGraphInputStore } from "../../../store/GraphInputStore";
import { getEventTextContent } from "../../../hooks/utils";

export interface SelectBoxProps {
  descriptionText: string;
  optionsList: Array<SelectBoxOptionValue>;
  itemKeyId: string;
  defaultValue: string | number | undefined;
  defaultText: string;
  getSelectValue: GetValueFunction;
  handleChange: HandleChangeEventFunction;
}

export type SelectBoxOptionValue = { value: string; text: string };

export const SelectBoxInput = ({
  descriptionText,
  optionsList,
  itemKeyId,
  defaultText,
  getSelectValue,
  handleChange,
}: SelectBoxProps) => {
  const [inputText, setInputText] = useState<string>(defaultText);
  const [inputPlaceholder, setInputPlaceholder] = useState<string>(defaultText);

  const optionValues = optionsList.map((option) =>
    option["text"].toLowerCase()
  );

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleChangeValue = (
    e: React.ChangeEvent<HTMLInputElement> | React.FormEvent<HTMLElement>,
    actualValue?: string
  ) => {
    const target_value = getEventTextContent(e);
    setInputText(target_value);
    console.log("target_value", target_value);
    console.log("optionsValues", optionValues);

    if (optionValues.includes(target_value.toLowerCase())) {
      setInputPlaceholder(target_value);
      handleChange(e, actualValue);
    }
  };

  useEffect(() => {
    if (clearClicked) {
      setInputText(defaultText);
    }
  }, [clearClicked, defaultText]);

  return (
    <Flex m={1}>
      <FormControl width={"inputSizes.defaultBox"} color={"ui.white"}>
        <FormLabel>{descriptionText}</FormLabel>
        <AutoComplete openOnFocus listAllValuesOnFocus value={getSelectValue()}>
          <AutoCompleteInput
            value={inputText}
            onChange={(e) => handleChangeValue(e)}
            onFocus={() => setInputText("")}
            onBlur={() => setInputText(inputPlaceholder || defaultText)}
            placeholder={inputPlaceholder}
            bgColor={"ui.input"}
            autoComplete="off"
          />
          <AutoCompleteList
            borderColor={"ui.grey"}
            bgColor="ui.input"
            margin={0}
            p={0}
            marginBottom={0}
            borderRadius={0}
            maxH={"150px"}
            overflowY={"auto"}
          >
            {optionsList.map((option) => (
              <AutoCompleteItem
                value={option["text"]}
                key={descriptionText + itemKeyId + option["value"]}
                style={{
                  color: "white",
                  backgroundColor: "#2d3333",
                  margin: 0,
                  borderRadius: 0,
                }}
                onClick={(e) => handleChangeValue(e, option["value"])}
              >
                {option["text"]}
              </AutoCompleteItem>
            ))}
          </AutoCompleteList>
        </AutoComplete>
      </FormControl>
    </Flex>
  );
};
