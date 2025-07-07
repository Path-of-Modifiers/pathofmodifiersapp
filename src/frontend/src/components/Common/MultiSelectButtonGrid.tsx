import {
  Box, Flex, FlexProps
} from "@chakra-ui/layout";
import { Button } from "@chakra-ui/react";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { TextWithUnderline } from "../Text/TextWithUnderline";
import { useEffect, useState } from "react";
import { useGraphInputStore } from "../../store/GraphInputStore";

interface MultiSelectProps {
  optionsName: string;
  options: string[];
  defaultSelectedOptions?: string[];
  setValue: (value: string) => void;
  removeValue: (value: string) => void;
  onClearClick?: () => void;
  flexProps?: FlexProps;
}

const MultiSelectButtonGrid = (props: MultiSelectProps) => {
  const options = props.options;
  const defaultSelectedOptions = props.defaultSelectedOptions;
  const numberOfOptions = options.length;

  let defaultSelectedOptionsBoolean: boolean[];
  if (defaultSelectedOptions !== undefined) {
    defaultSelectedOptionsBoolean = options.map((val) => defaultSelectedOptions.includes(val));
  } else {
    defaultSelectedOptionsBoolean = new Array<boolean>(numberOfOptions).fill(false);
  }

  const [selectedOptions, setSelectedOptions] = useState<boolean[]>(defaultSelectedOptionsBoolean);

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  useEffect(() => {
    if (clearClicked && props.onClearClick) {
      props.onClearClick();
      setSelectedOptions(defaultSelectedOptionsBoolean);
    }
  }, [clearClicked])

  const buttons = options.map((val, idx) => {
    return <Box textAlign="center" mr={2} mb={2} key={val}>
      <Button
        variant="solid"
        bg={selectedOptions[idx] ? "ui.lightInput" : "ui.input"}
        color="ui.white"
        _hover={{
          bg: "ui.grey"
        }}
        borderWidth={1}
        borderColor="ui.grey"
        maxW="bgBoxes.mediumPPBox"
        fontWeight="normal"
        onClick={() => {
          setSelectedOptions((currentSelectedOptions) => [
            ...currentSelectedOptions.slice(0, idx),
            !selectedOptions[idx],
            ...currentSelectedOptions.slice(idx + 1)])
          if (!selectedOptions[idx]) {
            props.setValue(val);
          } else {
            props.removeValue(val)
          }
        }}
      >
        {capitalizeFirstLetter(val)}
      </Button>
    </Box>
  })
  return <Flex direction="column">
    <TextWithUnderline text={props.optionsName} />
    <Flex
      direction="row"
      flexWrap="wrap"
      mt={2}
    >
      {...buttons}
    </Flex>
  </Flex>
}

export default MultiSelectButtonGrid;
