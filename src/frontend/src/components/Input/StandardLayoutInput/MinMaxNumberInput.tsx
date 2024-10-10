import { FlexProps } from "@chakra-ui/layout";
import {
  Flex,
  Text,
  NumberInputProps,
  NumberInput,
  NumberInputField,
} from "@chakra-ui/react";

type HandleNumberChangeEventFunction = (
  value: string,
  numericalType: string
) => void;

export interface MinMaxNumberProps {
  flexProps?: FlexProps;
  numberInputProps?: NumberInputProps;
  descriptionText?: string;
  index: number;
  handleNumberChange: HandleNumberChangeEventFunction;
  isDimmed?: boolean;
}

export const MinMaxNumberInput = (props: MinMaxNumberProps) => {
  return (
    <Flex
      {...props.flexProps}
      flexDirection="column"
      width={props.flexProps ? props.flexProps.width : "inputSizes.smallPPBox"}
      height={props.flexProps ? props.flexProps.height : "lineHeights.tall"}
    >
      {props.descriptionText && (
        <Text mb={2} fontSize={15} color="ui.white">
          {props.descriptionText}
        </Text>
      )}
      <Flex opacity={props.isDimmed ? 0.5 : 1} flexDirection="row">
        <NumberInput
          {...props.numberInputProps}
          onChange={(e) => props.handleNumberChange(e, "min")}
          mr={1}
        >
          <NumberInputField
            // h={5} only for  flexDirection="column"
            p={1}
            placeholder={"Min"}
            bgColor="ui.input"
            textAlign="center"
          />
        </NumberInput>
        <NumberInput
          {...props.numberInputProps}
          onChange={(e) => props.handleNumberChange(e, "max")}
        >
          <NumberInputField
            // h={5} only for  flexDirection="column"
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
