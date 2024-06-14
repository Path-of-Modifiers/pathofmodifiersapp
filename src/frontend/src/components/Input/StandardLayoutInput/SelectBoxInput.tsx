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

  const selectValue = getSelectValue();

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handeSetInputText = (e: React.ChangeEvent<HTMLInputElement>) => {
    const target_value = e.currentTarget.value;
    setInputText(target_value);
    handleChange(e);
  };

  const handleChangeWithText = (
    e: React.FormEvent<HTMLElement>,
    actual_value?: string
  ) => {
    setInputText(e.currentTarget.textContent || "");
    handleChange(e, actual_value);
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
        <AutoComplete openOnFocus listAllValuesOnFocus>
          <AutoCompleteInput
            value={inputText}
            onChange={(e) => handeSetInputText(e)}
            onFocus={() => setInputText("")}
            onBlur={() => setInputText(selectValue?.toString() || defaultText)}
            placeholder={inputText}
            autoComplete="off"
          />
          <AutoCompleteList
            borderColor={"ui.grey"}
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
                onClick={(e) => handleChangeWithText(e, option["value"])}
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
