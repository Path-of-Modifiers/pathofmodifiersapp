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
  optionsList: Array<SelectBoxOptionValue>;
  itemKeyId: string;
  defaultValue?: string;
  defaultText?: string;
  descriptionText?: string;
  getSelectValue?: GetValueFunction;
  handleChange: HandleChangeEventFunction;
  width?: string;
  noPlaceholder?: boolean;
}

export type SelectBoxOptionValue = { value: string | undefined; text: string };

export const SelectBoxInput = ({
  descriptionText,
  optionsList,
  itemKeyId,
  defaultValue,
  defaultText,
  handleChange,
  width,
  noPlaceholder,
}: SelectBoxProps) => {
  defaultText = defaultText || "";
  const [inputText, setInputText] = useState<string>(defaultText);
  const [inputPlaceholder, setInputPlaceholder] = useState<string>(
    noPlaceholder ? "" : defaultText
  );

  const optionValues = optionsList.map((option) =>
    option["text"].toLowerCase()
  );

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleChangeValue = (
    e: React.ChangeEvent<HTMLInputElement> | React.MouseEvent<HTMLElement>,
    actualValue?: string | undefined
  ) => {
    const target_value = getEventTextContent(e);
    setInputText(target_value);

    if (optionValues.includes(target_value.toLowerCase()) || !target_value) {
      if (!noPlaceholder) {
        setInputPlaceholder(target_value);
      } else {
        setInputText("");
      }
      handleChange(e, actualValue);
    }
  };

  useEffect(() => {
    if (clearClicked) {
      setInputText(defaultText || "");
    }
  }, [clearClicked, defaultText]);

  return (
    <Flex m={1}>
      <FormControl width={width || "inputSizes.defaultBox"} color={"ui.white"}>
        {descriptionText && (
          <FormLabel color={"ui.white"}>{descriptionText}</FormLabel>
        )}
        <AutoComplete
          openOnFocus
          listAllValuesOnFocus
          defaultValue={defaultValue}
          >
          <AutoCompleteInput
            value={inputText}
            onChange={(e) => handleChangeValue(e)}
            onFocus={() => setInputText("")}
            placeholder={inputPlaceholder}
            bgColor={"ui.input"}
            autoComplete="off"
            />
          <AutoCompleteList
            onBlur={() => setInputText(noPlaceholder ? "" : inputPlaceholder)}
            borderColor={"ui.grey"}
            bgColor="ui.input"
            margin={0}
            p={0}
            marginBottom={0}
            borderRadius={0}
            maxH={"200px"}
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
