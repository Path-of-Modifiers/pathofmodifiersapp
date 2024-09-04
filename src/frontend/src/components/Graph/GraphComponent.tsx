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
  const render = result && mostCommonCurrencyUsed && !isError;

  const showChaos = usePlotSettingsStore((state) => state.showChaos);
  const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

  if (fetchStatus === "fetching") {
    return (
      <Center>
        <Spinner size="xl" color={"ui.white"} />
      </Center>
    );
  }

  return (
    render && (
      <Box {...props}>
        <PlotCustomizationButtons
          flexProps={undefined}
          mostCommonCurrencyUsed={mostCommonCurrencyUsed}
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
                value: "Chaos value",
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
              dataKey="valueInChaos"
              name="Chaos value"
              stroke="#f99619"
              hide={!showChaos}
            />

            <YAxis
              label={{
                value: `${capitalizeFirstLetter(mostCommonCurrencyUsed)} value`,
                angle: -90,
                position: "right",
              }}
              orientation="right"
              yAxisId={1}
              hide={!showSecondary}
            />
            <Line
              type="monotone"
              dataKey="valueInMostCommonCurrencyUsed"
              name={`${capitalizeFirstLetter(mostCommonCurrencyUsed)} value`}
              stroke="ui.white"
              yAxisId={1}
              hide={!showSecondary}
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    )
  );
}

export default GraphComponent;
