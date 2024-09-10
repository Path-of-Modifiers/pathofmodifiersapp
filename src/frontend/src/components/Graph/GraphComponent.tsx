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

/**
 * Uses the globally stored plotQuery state to send a request,
 * the response is processed. Returns a spinner while retrieving
 * data. If no plotQuery has been set, no graph is returned.
 * @returns A spinner while loading data, nothing if no query yet
 * and a graph if there has been
 */
function GraphComponent(props: BoxProps) {
  const plotQuery = useGraphInputStore((state) => state.plotQuery);
  const { result, mostCommonCurrencyUsed, fetchStatus, isError } =
    useGetPlotData(plotQuery);

  const renderGraph = result && mostCommonCurrencyUsed && !isError;

  const showChaos = usePlotSettingsStore((state) => state.showChaos);
  const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

  const chaosVisuals: CurrencyVisuals = {
    stroke: "#f99619",
    name: "Chaos value",
    yAxisId: 0,
    datakey: "valueInChaos",
    buttonColor: "#000000",
    buttonBorderColor: "#000000",
    buttonBackground: showChaos ? "#f99619" : "ui.lightInput",
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
        <PlotCustomizationButtons
          flexProps={{ justifyContent: "center" }}
          mostCommonCurrencyUsed={mostCommonCurrencyUsed}
          chaosVisuals={chaosVisuals}
          secondaryVisuals={secondaryVisuals}
        />
        <ResponsiveContainer>
          <LineChart
            width={500}
            height={300}
            data={result}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            {/* Set Y-axis label */}
            <YAxis
              label={{
                value: chaosVisuals.name,
                angle: -90,
                position: "insideLeft",
              }}
              hide={!showChaos}
            />
            <Tooltip />
            <Legend verticalAlign="top" height={36} />
            {/* Update the Line dataKey to match "Chaos value" */}
            <Line
              type="monotone"
              dataKey={chaosVisuals.datakey}
              name={chaosVisuals.name}
              stroke={chaosVisuals.stroke}
              yAxisId={chaosVisuals.yAxisId}
              hide={!showChaos}
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
            />
            <Line
              type="monotone"
              dataKey={secondaryVisuals.datakey}
              name={secondaryVisuals.name}
              stroke={secondaryVisuals.stroke}
              yAxisId={secondaryVisuals.yAxisId}
              hide={!showSecondary}
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    )
  );
}

export default GraphComponent;
