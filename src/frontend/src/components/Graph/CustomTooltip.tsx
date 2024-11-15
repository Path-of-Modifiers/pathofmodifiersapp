import { Box, Divider } from "@chakra-ui/layout";
import { TooltipProps } from "recharts";
// for recharts v2.1 and above
import {
  ValueType,
  NameType,
} from "recharts/types/component/DefaultTooltipContent";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { BiError } from "react-icons/bi";

export const CustomTooltip = ({
  active,
  payload,
  label,
}: TooltipProps<ValueType, NameType>) => {
  if (active && payload && payload.length) {
    const days = Math.floor(label / 24);
    const hours = label % 24;

    const confidence = payload[0].payload.confidence;
    const isLowConfidence = confidence === "low";
    const isMediumConfidence = confidence === "medium";
    const confidenceColor = isLowConfidence
      ? "#bf0118"
      : isMediumConfidence
        ? "#facc14"
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
        <Box my="5px">
          {`${days} days`}
          {hours && ` and ${hours} hours`}
          {" since launch"}
        </Box>
        <Divider />
        <Box display="flex" flexDirection="row">
          <Box>Confidence: </Box>
          <Box textAlign="right" ml="auto">
            {capitalizeFirstLetter(confidence)}
          </Box>
          <Box>
            {isLowConfidence && (
              <BiError
                color={confidenceColor}
                size="1.5rem"
                key="low-confidence"
              />
            )}
            {isMediumConfidence && (
              <BiError
                color={confidenceColor}
                size="1.5rem"
                key="medium-confidence"
              />
            )}
          </Box>
        </Box>

        <Divider mb="5px" />
        {payload.map((value, index) => (
          <Box display="flex" flexDirection="row" key={`value-${index}`}>
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
