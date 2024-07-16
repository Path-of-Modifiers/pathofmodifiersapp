import { Flex, Text } from "@chakra-ui/layout";
import { Select } from "@chakra-ui/react";
import { GetValueFunction, HandleChangeEventFunction } from "../../../schemas/function/InputFunction";


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

export const SelectBox = ({
  descriptionText,
  optionsList,
  itemKeyId,
  defaultValue,
  defaultText,
  getSelectValue,
  handleChange,
}: SelectBoxProps) => {
  return (
    <Flex alignItems="center" bgColor={"ui.secondary"} color={"ui.white"} m={1}>
      <Text
        ml={1}
        width={"inputSizes.defaultDescriptionText"}
        fontSize="defaultRead"
      >
        {descriptionText}
      </Text>
      <Select
        value={getSelectValue()}
        bgColor={"ui.input"}
        onChange={(e) => handleChange(e)}
        width={"inputSizes.defaultBox"}
        color={"ui.white"}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={{ descriptionText } + itemKeyId}
      >
        {
          <option
            value={defaultValue}
            key={descriptionText + itemKeyId + "_undefined"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            {defaultText}
          </option>
        }
        ,
        {optionsList.map((option) => {
          return (
            <option
              value={option["value"]}
              key={descriptionText + itemKeyId + option["value"]}
              style={{ color: "white", backgroundColor: "#2d3333" }}
            >
              {option["text"]}
            </option>
          );
        })}
      </Select>
    </Flex>
  );
};
