import { Flex, Text } from "@chakra-ui/layout";
import { Select } from "@chakra-ui/react";

export interface SelectBoxProps {
  descriptionText: string;
  optionsList: Array<SelectBoxOptionValue>;
  itemKeyId: string;
  defaultValue: string | number | undefined;
  defaultText: string;
  getSelectValue: SelectBoxGetValue;
  handleChange: SelectBoxHandleChange;
}

export type SelectBoxOptionValue = { value: string; text: string };

type SelectBoxGetValue = () => string | number | undefined;

type SelectBoxHandleChange = (
  event: React.ChangeEvent<HTMLSelectElement>
) => void;

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
      <Text ml={1} width={"inputSizes.defaultDescriptionText"} fontSize="defaultRead">
        {descriptionText}
      </Text>
      <Select
        value={getSelectValue()}
        bgColor={"ui.input"}
        onChange={(e) => handleChange(e)}
        width={"inputSizes.defaultSelect"}
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
