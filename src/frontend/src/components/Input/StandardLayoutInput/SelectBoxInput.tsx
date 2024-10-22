/* eslint-disable @typescript-eslint/no-explicit-any */

import {
  FormControlProps,
  FormControl,
  FormLabel,
  Flex,
  FlexProps,
} from "@chakra-ui/react";
import {
  Select,
  SingleValue,
  OptionBase,
  ChakraStylesConfig,
} from "chakra-react-select";
import { useEffect, useState } from "react";
import { useGraphInputStore } from "../../../store/GraphInputStore";

interface NewValue {
  label: string;
  value: string;
}

export type HandleChangeEventFunction = (
  newValue: SingleValue<NewValue> | undefined,
  overrideIndex?: number
) => void;

export interface SelectBoxOptionValue {
  value: string;
  label: string;
  regex: string;
}

export interface SelectBoxProps {
  formControlProps?: FormControlProps;
  flexProps?: FlexProps;
  optionsList: Array<SelectBoxOptionValue>;
  handleChange: HandleChangeEventFunction;
  defaultText: string | undefined;
  multipleValues: boolean;
  id: string;
  isDimmed?: boolean;
  descriptionText?: string;
  canBeAny?: boolean;
  autoFocus?: boolean;
  unstyled?: boolean;
}

interface SelectOption extends OptionBase {
  label: string;
  value: string;
}

export const SelectBoxInput = (props: SelectBoxProps) => {
  const handleChangeExternal = props.handleChange;
  const [placeholder, setPlaceholder] = useState<string | null>(null);
  const [inFocus, setInFocus] = useState<boolean>(false);

  let optionList = props.optionsList;
  // Adds the "Any" option
  if (props.canBeAny) {
    optionList = [{ value: "Any", label: "Any", regex: "Any" }, ...optionList];
  }
  let defaultValue: SelectOption;
  if (props.defaultText) {
    defaultValue = {
      label: props.defaultText,
      value: props.defaultText,
    };
  } else {
    defaultValue = optionList[0];
  }
  const [selectedValue, setSelectedValue] = useState<SelectOption | null>(
    defaultValue
  );

  const { clearClicked } = useGraphInputStore();
  useEffect(() => {
    if (clearClicked) {
      setSelectedValue(null);
    }
  }, [clearClicked, setSelectedValue]);

  // A custom filter function. Uses the `regex` attribute of `SelectOption`
  // to filter if the input starts with `~`.
  const customFilter = (
    candidate: { label: string; value: string; data: any },
    inputValue: string
  ): boolean => {
    const advancedSearch = inputValue.at(0) === "~";
    const lowerCaseInputValue = inputValue.toLowerCase();
    const lowerCaseCandidate = candidate.data.regex.toLowerCase();
    if (advancedSearch) {
      // The .slice(1) removes the initial `~`
      const splitString = lowerCaseInputValue.slice(1).split(" ");
      const regexString = splitString
        .map((subStr) => (subStr ? `(?=.*${subStr})` : ""))
        .join("");
      const regex = RegExp(regexString, "g");
      return regex.test(lowerCaseCandidate);
    } else {
      return lowerCaseCandidate.includes(lowerCaseInputValue);
    }
  };

  const handleChangeInternal: HandleChangeEventFunction = (newValue) => {
    if (newValue != null) {
      const newSelectedValue: SelectOption = {
        label: newValue.label,
        value: newValue.value,
      };
      setSelectedValue(newSelectedValue);
    }
  };

  const handleFocus = () => {
    setInFocus(true);
    if (selectedValue) {
      setPlaceholder(selectedValue.label);
    }
    setSelectedValue(null);
  };
  useEffect(() => {
    if (inFocus) {
      return;
    }
    if (selectedValue != null && !clearClicked) {
      return;
    }
    const prevOptionSelected = optionList.find(
      (option) => option.label === placeholder
    );
    if (prevOptionSelected === undefined) {
      setSelectedValue(defaultValue);
      return;
    }
    const prevSelectedValue: SelectOption = {
      label: prevOptionSelected.label,
      value: prevOptionSelected.value,
    };
    setSelectedValue(prevSelectedValue);
  }, [
    selectedValue,
    placeholder,
    optionList,
    inFocus,
    clearClicked,
    defaultValue,
  ]);

  const chakraStylesBase = {
    background: "ui.input",
    borderColor: "ui.grey",
  };

  // A bit verbose, but necessary to style the Chakra-react-select Chakra Add-On
  const chakraStyles: ChakraStylesConfig<SelectOption> = {
    dropdownIndicator: (provided) => ({
      ...provided,
      ...chakraStylesBase,
      p: 0,
      marginBottom: 0,
      overflowY: "auto",
      opacity: props.unstyled ? 0 : 1,
    }),
    container: (provided) => ({
      ...provided,
      ...chakraStylesBase,
      p: 0,
      marginBottom: 0,
      opacity: props.isDimmed ? 0.5 : 1,
      borderRadius: "lg",
      h: props.unstyled ? 5 : undefined,
    }),
    option: (provided) => ({
      ...provided,
      ...chakraStylesBase,
      _hover: {
        bgColor: "ui.secondary",
      },
    }),
    menuList: (provided) => ({
      ...provided,
      ...chakraStylesBase,
      minW: props.unstyled ? "13rem" : undefined,
      maxH: ["8rem", "15rem"],
    }),
  };

  return (
    <Flex
      {...props.flexProps}
      flexDirection={"row"}
      width={props.flexProps ? props.flexProps.width : "inputSizes.smallPPBox"}
    >
      <FormControl color={"ui.white"}>
        {props.descriptionText && (
          <FormLabel color={"ui.white"} fontSize="14px">
            {props.descriptionText}
          </FormLabel>
        )}
        <Select<SelectOption>
          variant={props.unstyled ? "unstyled" : "outline"}
          placeholder={placeholder ? placeholder : props.defaultText}
          options={optionList}
          onChange={(newValue) => {
            handleChangeInternal(newValue);
            handleChangeExternal(newValue);
            if (props.multipleValues) {
              setSelectedValue(null);
            }
          }}
          blurInputOnSelect={true}
          filterOption={(option, inputValue) =>
            customFilter(option, inputValue)
          }
          onFocus={handleFocus}
          onBlur={() => setInFocus(false)}
          value={selectedValue}
          selectedOptionColorScheme="#1B1B1B"
          chakraStyles={chakraStyles}
          autoFocus={props.autoFocus ?? false}
          openMenuOnFocus={true}
          focusBorderColor="ui.white"
          key={`${props.id}`}
        />
      </FormControl>
    </Flex>
  );
};
