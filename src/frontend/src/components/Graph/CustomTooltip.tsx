import { useState, useEffect } from "react"

import { Box, Divider, Text } from "@chakra-ui/layout";
import { TooltipProps } from "recharts";
import { Icon } from "@chakra-ui/react";

// for recharts v2.1 and above
import {
  ValueType,
  NameType,
} from "recharts/types/component/DefaultTooltipContent";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { BiError } from "react-icons/bi";
import {
  getHoursSinceLaunch,
} from "../../hooks/graphing/utils";
import { setupHourlyUpdate } from "../../utils";

interface CustomTooltipProps extends TooltipProps<ValueType, NameType> {
  upperBoundry: number;
  fetchedLeagues: string[];
  colors: string[]
}

export const CustomTooltip = (props: CustomTooltipProps) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  const hoursAgo = getHoursSinceLaunch(currentTime) - props.label

  const daysToDisplay = Math.floor(hoursAgo / 24)
  const hoursToDisplay = hoursAgo % 24


  useEffect(() => {
    return setupHourlyUpdate(setCurrentTime)
  }, []);



  if (props.active && props.payload && props.payload.length) {

    const confidence = props.payload[0].payload.confidence;
    const isLowConfidence = confidence === "low";
    const isMediumConfidence = confidence === "medium";
    const confidenceColor = isLowConfidence
      ? "ui.lowConfidencePrimary"
      : isMediumConfidence
        ? "ui.mediumConfidencePrimary"
        : "ui.input";
    return (
      <Box
        color="ui.white"
        display="flex"
        bgColor="ui.input"
        border="1px"
        borderRadius="lg"
        borderColor="ui.grey"
        p={1}
        whiteSpace="preserve"
        w="100%"
        flexDirection="column"
      >
        <Text my="5px">
          {hoursAgo !== 0 && daysToDisplay !== 0 && ` ${daysToDisplay} days ago`}
          {hoursAgo !== 0 && hoursToDisplay !== 0 && ` ${hoursToDisplay} hours ago`}
          {hoursAgo === 0 && ` now`}
        </Text>
        <Divider />
        <Box alignItems="center" display="flex" flexDirection="row">
          <Text>Confidence: </Text>
          <Text textAlign="right" ml="auto">
            {capitalizeFirstLetter(confidence)}
          </Text>
          <Box mt={1}>
            {isLowConfidence && (
              <Icon
                as={BiError}
                color={confidenceColor}
                boxSize="1.5rem"
                key="low-confidence"
              />
            )}
            {isMediumConfidence && (
              <Icon
                as={BiError}
                color={confidenceColor}
                boxSize="1.5rem"
                key="medium-confidence"
              />
            )}
          </Box>
        </Box>
        {(props.payload[0].value as number) > props.upperBoundry && (
          <Box>
            <Divider />
            <Box display="flex" flexDirection="row" alignContent="center">
              <Icon
                as={BiError}
                color="ui.lowConfidencePrimary"
                boxSize="1.5rem"
                key="medium-confidence"
              />
              <Text mx="auto" color="ui.lowConfidencePrimary">
                This is an outlier
              </Text>
              <Icon
                as={BiError}
                color="ui.lowConfidencePrimary"
                boxSize="1.5rem"
                key="medium-confidence"
              />
            </Box>
          </Box>
        )}

        <Divider mb="5px" />
        {props.payload.map((value, index) => (
          <Box display="flex" flexDirection="row" key={`value-${index}`} color={props.colors[props.fetchedLeagues.indexOf((value.name as string).split(" - ")[0])]}>
            <Box>{`${value.name}: `}</Box>
            <Box
              textAlign="right"
              ml="auto"
            >{`${(value.value as number).toFixed(2)}`}</Box>
          </Box>
        ))}
      </Box>
    );
  }

  return null;
};
