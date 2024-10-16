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
import { useState } from "react";

interface NewValue {
  label: string;
  value: string;
}

export type HandleChangeEventFunction = (
  newValue: SingleValue<NewValue>,
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
  presetIndex?: number;
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
  const [selectedValue, setSelectedValue] = useState<SelectOption | null>(null);
  let defaultOptionText: string | undefined = undefined;
  if (props.presetIndex !== undefined) {
    const defaultOption = props.optionsList.find(
      (option) => option.label === props.defaultText
    );
    defaultOptionText = defaultOption ? defaultOption.label : undefined;
  }

  let optionList = props.optionsList;

  // Adds the "Any" option
  if (props.canBeAny) {
    optionList = [{ value: "Any", label: "Any", regex: "Any" }, ...optionList];
  }

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
    if (newValue) {
      const newSelectedValue: SelectOption = {
        label: newValue.label,
        value: newValue.value,
      };
      setSelectedValue(newSelectedValue);
    }
  };

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
      maxH: "200px",
      overflowY: "auto",
    }),
    container: (provided) => ({
      ...provided,
      ...chakraStylesBase,
      p: 0,
      marginBottom: 0,
      opacity: props.isDimmed ? 0.5 : 1,
      borderRadius: "lg",
      w: props.unstyled ? "10vw" : undefined,
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
    }),
  };

  return (
    <Flex
      {...props.flexProps}
      marginTop={0}
      marginBottom={0}
      flexDirection={"row"}
      alignItems={"center"}
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
          placeholder={props.defaultText}
          options={optionList}
          onChange={(newValue) => {
            handleChangeInternal(newValue);
            if (props.presetIndex !== undefined) {
              handleChangeExternal(newValue, props.presetIndex);
            } else {
              handleChangeExternal(newValue);
              if (props.multipleValues) {
                setSelectedValue(null);
              }
            }
          }}
          closeMenuOnSelect={true}
          filterOption={(option, inputValue) =>
            customFilter(option, inputValue)
          }
          value={selectedValue}
          selectedOptionColorScheme="#1B1B1B"
          chakraStyles={chakraStyles}
          defaultInputValue={defaultOptionText}
          autoFocus={props.autoFocus ?? false}
          openMenuOnFocus={true}
          focusBorderColor="ui.white"
          key={`${props.id}`}
        />
      </FormControl>
    </Flex>
  );
};
