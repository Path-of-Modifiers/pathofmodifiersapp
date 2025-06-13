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
import { useGraphInputStore } from "../../store/GraphInputStore";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";
import PlotCustomizationButtons from "../Common/PlotCustomizationButtons";
import { capitalizeFirstLetter } from "../../hooks/utils";
import { CurrencyVisuals } from "../../schemas/CurrencyVisuals";
import { CustomTooltip } from "./CustomTooltip";
import {
  findWinsorUpperBound,
  formatHoursSinceLaunch,
} from "../../hooks/graphing/utils";
import { BiError } from "react-icons/bi";
import { ErrorMessage } from "../Input/StandardLayoutInput/ErrorMessage";
import usePostPlottingData from "../../hooks/graphing/postPlottingData";
import useCustomToast from "../../hooks/useCustomToast";
import { useEffect } from "react";

/**
 * Uses the globally stored plotQuery state to send a request,
 * the response is processed. Returns a spinner while retrieving
 * data. If no plotQuery has been set, no graph is returned.
 * @returns A spinner while loading data, nothing if no query yet
 * and a graph if there has been
 */
function GraphComponent(props: BoxProps) {
  const { plotQuery } = useGraphInputStore();
  const { plotData, fetchStatus, isFetched, isError, error } =
    usePostPlottingData(plotQuery);

  const showToast = useCustomToast();
  useEffect(() => {
    if (isError && isFetched) {
      if (error != null) {
        showToast("Plotting error", error.message, "error");
      }
    }
  }, [isError, isFetched, error, showToast]);

  const mostCommonCurrencyUsed = plotData?.mostCommonCurrencyUsed;
  const renderGraph =
    plotData != undefined && mostCommonCurrencyUsed != undefined && !error;
  const showChaos = usePlotSettingsStore((state) => state.showChaos);
  const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

  if (error || plotData == undefined) return;

  const confidenceRating = plotData.data[0].confidenceRating;
  const isLowConfidence = confidenceRating === "low";
  const isMediumConfidence = confidenceRating === "medium";
  const confidenceColor = isLowConfidence
    ? "ui.lowConfidencePrimary"
    : isMediumConfidence
      ? "ui.mediumConfidencePrimary"
      : "ui.input";
  const upperBoundryChaos = findWinsorUpperBound(
    plotData.data[0].data.reduce(
      (prev, cur) => [...prev, cur.valueInChaos],
      [] as number[]
    )
  );
  const upperBoundrySecondary = findWinsorUpperBound(
    plotData.data[0].data.reduce(
      (prev, cur) => [...prev, cur.valueInMostCommonCurrencyUsed],
      [] as number[]
    )
  );

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
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 25,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="hoursSinceLaunch"
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
            {plotData.data.map((series) => (
              <Line
                type="monotone"
                data={series.data}
                dataKey={chaosVisuals.datakey}
                key={series.name}
                name={series.name + " - " + chaosVisuals.name}
                stroke={chaosVisuals.stroke}
                yAxisId={chaosVisuals.yAxisId}
                hide={!showChaos}
                isAnimationActive={false}
                dot={{ fill: chaosVisuals.stroke }}
              />
            ))}
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
            {plotData.data.map((series) => (
              <Line
                type="monotone"
                data={series.data}
                dataKey={secondaryVisuals.datakey}
                key={series.name}
                name={series.name + " - " + secondaryVisuals.name}
                stroke={secondaryVisuals.stroke}
                yAxisId={secondaryVisuals.yAxisId}
                hide={!showSecondary}
                isAnimationActive={false}
                dot={{ fill: secondaryVisuals.stroke }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </Box>
    )
  );
}

export default GraphComponent;
