import { FlexProps } from "@chakra-ui/layout";
import {
  Flex,
  Text,
  NumberInputProps,
  NumberInput,
  NumberInputField,
} from "@chakra-ui/react";

export type HandleNumberChangeEventFunction = (
  value: string,
  numericalType: string
) => void;

export interface DefaultMinMaxValues {
  min?: number;
  max?: number;
}

export interface MinMaxNumberProps {
  flexProps?: FlexProps;
  numberInputProps?: NumberInputProps;
  descriptionText?: string;
  handleNumberChange: HandleNumberChangeEventFunction;
  isDimmed?: boolean;
  defaultValues?: DefaultMinMaxValues;
  tight?: boolean;
}

export const MinMaxNumberInput = (props: MinMaxNumberProps) => {
  return (
    <Flex
      {...props.flexProps}
      flexDirection={"column"}
      width={props.flexProps ? props.flexProps.width : "inputSizes.smallPPBox"}
      height={props.flexProps ? props.flexProps.height : "lineHeights.tall"}
      color="ui.white"
    >
      {props.descriptionText && (
        <Text mb={2} fontSize={15} color="ui.white">
          {props.descriptionText}
        </Text>
      )}
      <Flex opacity={props.isDimmed ? 0.5 : 1}>
        <NumberInput
          {...props.numberInputProps}
          id="number-input-min"
          onChange={(e) => props.handleNumberChange(e, "min")}
          mr={1}
          defaultValue={
            props.defaultValues?.min ? props.defaultValues.min : undefined
          }
          onBlurCapture={(e) => {
            if (e.relatedTarget != null) {
              if (e.relatedTarget.id === "number-input-max") {
                e.stopPropagation();
              }
            }
          }}
          focusBorderColor="ui.white"
        >
          <NumberInputField
            h={props.tight ? 5 : undefined}
            w={props.tight ? 10 : undefined}
            autoFocus={props.defaultValues ? true : false}
            p={1}
            placeholder={"Min"}
            bgColor="ui.input"
            textAlign="center"
          />
        </NumberInput>
        <NumberInput
          {...props.numberInputProps}
          id="number-input-max"
          onChange={(e) => props.handleNumberChange(e, "max")}
          defaultValue={
            props.defaultValues?.max ? props.defaultValues.max : undefined
          }
          onBlurCapture={(e) => {
            if (e.relatedTarget != null) {
              if (e.relatedTarget.id === "number-input-min") {
                e.stopPropagation();
              }
            }
          }}
          focusBorderColor="ui.white"
        >
          <NumberInputField
            h={props.tight ? 5 : undefined}
            w={props.tight ? 10 : undefined}
            p={1}
            placeholder={"Max"}
            bgColor="ui.input"
            textAlign="center"
          />
        </NumberInput>
      </Flex>
    </Flex>
  );
};
