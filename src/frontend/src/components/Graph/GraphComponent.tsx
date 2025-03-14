import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Box, BoxProps, Center, Spinner } from "@chakra-ui/react";
import useGetPlotData from "../../hooks/graphing/processPlottingData";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";
import PlotCustomizationButtons from "../Common/PlotCustomizationButtons";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { CurrencyVisuals } from "../../schemas/CurrencyVisuals";
import { CustomTooltip } from "./CustomTooltip";
import { formatHoursSinceLaunch } from "../../hooks/graphing/utils";
import { BiError } from "react-icons/bi";
import { ErrorMessage } from "../Input/StandardLayoutInput/ErrorMessage";

/**
 * Uses the globally stored plotQuery state to send a request,
 * the response is processed. Returns a spinner while retrieving
 * data. If no plotQuery has been set, no graph is returned.
 * @returns A spinner while loading data, nothing if no query yet
 * and a graph if there has been
 */
function GraphComponent(props: BoxProps) {
  const { plotQuery } = useGraphInputStore();
  const {
    result,
    mostCommonCurrencyUsed,
    confidenceRating,
    upperBoundryChaos,
    upperBoundrySecondary,
    fetchStatus,
    error,
  } = useGetPlotData(plotQuery);

  const renderGraph = result && mostCommonCurrencyUsed && !error;
  const showChaos = usePlotSettingsStore((state) => state.showChaos);
  const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

  if (error) return;

  const isLowConfidence = confidenceRating === "low";
  const isMediumConfidence = confidenceRating === "medium";
  const confidenceColor = isLowConfidence
    ? "ui.lowConfidencePrimary"
    : isMediumConfidence
      ? "ui.mediumConfidencePrimary"
      : "ui.input";

  const chaosVisuals: CurrencyVisuals = {
    stroke: "#f99619",
    name: "Chaos value",
    yAxisId: 0,
    datakey: "valueInChaos",
    buttonColor: "#000000",
    buttonBorderColor: "#000000",
    buttonBackground: showChaos ? "#f99619" : "ui.lightInput",
    upperBoundry: upperBoundryChaos,
  };

  const secondaryVisuals: CurrencyVisuals = {
    stroke: "#ff0000",
    name: renderGraph
      ? `${capitalizeFirstLetter(mostCommonCurrencyUsed)} value`
      : "",
    yAxisId: 1,
    datakey: "valueInMostCommonCurrencyUsed",
    buttonColor: showSecondary ? "#ff0000" : "#000000",
    buttonBorderColor: showSecondary ? "#ff0000" : "#000000",
    buttonBackground: showSecondary ? "ui.white" : "ui.lightInput",
    upperBoundry: upperBoundrySecondary,
  };

  if (fetchStatus === "fetching") {
    return (
      <Center>
        <Spinner size="xl" color={"ui.white"} />
      </Center>
    );
  }
  if (error) return;

  return (
    renderGraph && (
      <Box {...props}>
        <Box>
          {isLowConfidence && (
            <ErrorMessage
              alertTitle="Low confidence"
              alertDescription="Prices are based on a low number of listings."
              alertIcon={BiError}
              iconProps={{
                color: confidenceColor,
                size: "1.5rem",
              }}
              alertProps={{
                bgColor: "ui.lowConfidenceSecondary",
                color: "white",
              }}
            />
          )}
          {isMediumConfidence && (
            <ErrorMessage
              alertTitle="Medium confidence"
              alertDescription="Prices are based on a relatively low number of listings."
              alertIcon={BiError}
              iconProps={{
                color: confidenceColor,
                size: "1.5rem",
              }}
              alertProps={{
                bgColor: "ui.mediumConfidenceSecondary",
                color: "white",
              }}
            />
          )}
          <PlotCustomizationButtons
            flexProps={{ justifyContent: "center", mt: "10px" }}
            mostCommonCurrencyUsed={mostCommonCurrencyUsed}
            chaosVisuals={chaosVisuals}
            secondaryVisuals={secondaryVisuals}
          />
        </Box>
        <ResponsiveContainer>
          <LineChart
            width={500}
            height={300}
            data={result}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 25,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="timestamp"
              label={{
                value: "Days and hours since launch",
                position: "bottom",
              }}
              angle={0}
              tickMargin={11}
              minTickGap={13}
              tickFormatter={(value) => formatHoursSinceLaunch(value)}
              type="number"
              domain={["dataMin", "dataMax + 10"]}
            />
            {/* Set Y-axis label */}
            <YAxis
              label={{
                value: chaosVisuals.name,
                angle: -90,
                position: "insideLeft",
              }}
              hide={!showChaos}
              type="number"
              dataKey={chaosVisuals.datakey}
              domain={[0, chaosVisuals.upperBoundry]}
              allowDataOverflow
            />
            <Tooltip
              content={<CustomTooltip upperBoundry={upperBoundryChaos} />}
              isAnimationActive={false}
            />
            <Legend verticalAlign="top" height={36} />
            {/* Update the Line dataKey to match "Chaos value" */}
            <Line
              type="monotone"
              dataKey={chaosVisuals.datakey}
              name={chaosVisuals.name}
              stroke={chaosVisuals.stroke}
              yAxisId={chaosVisuals.yAxisId}
              hide={!showChaos}
              isAnimationActive={false}
              dot={{ fill: chaosVisuals.stroke }}
            />

            <YAxis
              label={{
                value: secondaryVisuals.name,
                angle: -90,
                position: "right",
              }}
              orientation="right"
              yAxisId={secondaryVisuals.yAxisId}
              hide={!showSecondary}
              type="number"
              domain={[0, secondaryVisuals.upperBoundry]}
              allowDataOverflow
            />
            <Line
              type="monotone"
              dataKey={secondaryVisuals.datakey}
              name={secondaryVisuals.name}
              stroke={secondaryVisuals.stroke}
              yAxisId={secondaryVisuals.yAxisId}
              hide={!showSecondary}
              isAnimationActive={false}
              dot={{ fill: secondaryVisuals.stroke }}
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    )
  );
}

export default GraphComponent;
