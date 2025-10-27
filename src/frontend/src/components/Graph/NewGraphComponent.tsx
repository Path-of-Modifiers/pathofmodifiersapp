import { Box, BoxProps, Center } from "@chakra-ui/layout";
import usePostPlottingData from "../../hooks/graphing/postPlottingData";
import { capitalizeFirstLetter } from "../../hooks/utils";
import PlotCustomizationButtons from "../Common/PlotCustomizationButtons";
import {
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatHoursSinceLaunch } from "../../hooks/graphing/utils";
import { Spinner } from "@chakra-ui/react";
import { usePlotSettingsStore } from "../../store/PlotSettingsStore";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { CustomTooltip } from "./CustomTooltip";
import useCustomToast from "../../hooks/useCustomToast";
import { useEffect } from "react";

function GraphComponent(props: BoxProps) {
  const { plotQuery, leagues } = useGraphInputStore();
  const { plotData, fetchStatus, error, isError, isFetched } =
    usePostPlottingData(plotQuery);

  const showChaos = usePlotSettingsStore((state) => state.showChaos);
  const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

  const showToast = useCustomToast();
  useEffect(() => {
    if (isError && isFetched) {
      if (error != null) {
        showToast("Plotting error", error.message, "error");
      }
    }
  }, [isError, isFetched, error, showToast]);
  if (error || plotData == undefined) return;
  const mostCommonCurrencyUsed = plotData.mostCommonCurrencyUsed;
  const mostCommonCurrencyUsedName = `${capitalizeFirstLetter(mostCommonCurrencyUsed ?? "")} value`;

  const renderGraph =
    plotData != undefined && mostCommonCurrencyUsed != undefined && !error;

  const fetchedLeagues = plotData.data.map((val) => val.league);

  const colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
  ];

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
          flexProps={{ justifyContent: "center", mt: "10px" }}
          mostCommonCurrencyUsed={mostCommonCurrencyUsed}
        />
        <ResponsiveContainer>
          <ScatterChart>
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
                value: "Chaos value",
                angle: -90,
                position: "insideLeft",
              }}
              hide={!showChaos}
              type="number"
              dataKey={"valueInChaos"}
              // domain={[0, upperBoundryChaos]}
              allowDataOverflow
            />
            <Tooltip
              content={
                <CustomTooltip
                  upperBoundry={1000}
                  fetchedLeagues={fetchedLeagues}
                  colors={colors}
                />
              }
              isAnimationActive={false}
            />
            <Legend verticalAlign="top" height={36} />
            {plotData.data.map((leagueData, idx) => {
              console.log(leagueData);
              return (
                leagues.includes(leagueData.league) && (
                  <Scatter
                    data={leagueData.linkedPrices.map(
                      (linkedPrices) => linkedPrices.data
                    )}
                    dataKey={"valueInChaos"}
                    line
                    key={leagueData.league}
                    name={leagueData.league + " - " + "Chaos Value"}
                    stroke={colors[idx]}
                    yAxisId={0}
                    hide={!showChaos}
                    isAnimationActive={false}
                    // dot={{ fill: colors[idx] }}
                    legendType={showChaos ? "line" : "none"}
                  />
                )
              );
            })}
            <YAxis
              label={{
                value: mostCommonCurrencyUsedName,
                angle: -90,
                position: "right",
              }}
              orientation="right"
              yAxisId={1}
              hide={!showSecondary}
              type="number"
              dataKey={"valueInMostCommonCurrencyUsed"}
              // domain={[0, upperBoundrySecondary]}
              allowDataOverflow
            />
          </ScatterChart>
        </ResponsiveContainer>
      </Box>
    )
  );
}

export default GraphComponent;
