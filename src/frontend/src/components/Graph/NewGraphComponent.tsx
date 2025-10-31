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
import useCustomToast from "../../hooks/useCustomToast";
import { useEffect, useState } from "react";

const colors = [
  "#1f77b4",
  "#ff7f0e",
  "#2ca02c",
  "#d62728",
  "#9467bd",
  "#8c564b",
  "#e377c2",
  "#bcbd22",
  "#17becf",
];

const shadedColors = [
  "#0f476e",
  "#9e4c05",
  "#176117",
  "#841415",
  "#5a3d74",
  "#55322b",
  "#8c4777",
  "#737411",
  "#0a757f",
];

// type onEvent = (gameItemId: string) => void;

// interface ScatterBase {
//   data: LinkedPrices | LeagueData;
//   dataKey: string;
//   idx: number;
//   yAxisId: number;
//   hide: boolean;
// }

// interface ScatterWithLabel extends ScatterBase {
//   league: string;
//   currencyName: string;
//   showLabel: boolean;
// }

// interface LinkedScatterProps extends ScatterWithLabel {
//   data: LinkedPrices;
//   handleHoverLinked: onEvent;
//   handleDoneHoveringLinked: onEvent;
//   handleClickedLinked: onEvent;
// }
// interface HighlightScatterProps extends LinkedScatterProps {
//   highlightColor?: string;
// }

// interface UnlinkedScatterProps extends ScatterWithLabel {
//   data: LeagueData;
// }

// function HighLightedScatter(props: HighlightScatterProps) {
//   const {
//     data,
//     dataKey,
//     hide,
//     idx,
//     yAxisId,
//     league,
//     currencyName,
//     handleHoverLinked,
//     handleDoneHoveringLinked,
//     handleClickedLinked,
//   } = props;
//   let { highlightColor } = props;
//   if (highlightColor === undefined) highlightColor = "#FFF";
//   return (
//     <Scatter
//       data={data.data}
//       dataKey={dataKey}
//       hide={hide}
//       yAxisId={yAxisId}
//       line
//       name={league + " - " + currencyName + " value"}
//       key={data.gameItemId + "_highlighted"}
//       fill={colors[idx]}
//       stroke={highlightColor}
//       isAnimationActive={false}
//       onMouseOver={() => handleHoverLinked(data.gameItemId)}
//       onMouseOut={() => handleDoneHoveringLinked(data.gameItemId)}
//       onClick={() => handleClickedLinked(data.gameItemId)}
//     />
//   );
// }

// function LinkedScatter(props: LinkedScatterProps) {
//   const {
//     data,
//     dataKey,
//     hide,
//     idx,
//     yAxisId,
//     handleHoverLinked,
//     handleDoneHoveringLinked,
//     handleClickedLinked,
//   } = props;
//   return (
//     <Scatter
//       data={data.data}
//       dataKey={dataKey}
//       key={data.gameItemId}
//       fill={colors[idx]}
//       stroke={colors[idx]}
//       yAxisId={yAxisId}
//       hide={hide}
//       isAnimationActive={false}
//       legendType={"none"}
//       onMouseOver={() => handleHoverLinked(data.gameItemId)}
//       onMouseOut={() => handleDoneHoveringLinked(data.gameItemId)}
//       onClick={() => handleClickedLinked(data.gameItemId)}
//     />
//   );
// }

// const UnlinkedScatter = (props: UnlinkedScatterProps) => {
//   const { data, dataKey, hide, idx, yAxisId, league, currencyName, showLabel } =
//     props;
//   // const { data, idx, yAxisId, dataKey } = props;
//   console.log("yo!");
//   return (
//     data.unlinkedPrices && (
//       <Scatter
//         data={data.unlinkedPrices}
//         dataKey={dataKey}
//         key={league + "_unlinked"}
//         fill={colors[idx]}
//         stroke={colors[idx]}
//         yAxisId={yAxisId}
//         hide={hide}
//         isAnimationActive={false}
//         legendType={showLabel ? "line" : "none"}
//         name={data.league + " - " + currencyName + " value"}
//       />
//     )
//   );
// };

function GraphComponent(props: BoxProps) {
  const { plotQuery, leagues } = useGraphInputStore();
  plotQuery.start = 0;
  // plotQuery.end = 300;
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

  const [gameItemIdsToShow, setGameItemIdsToShow] = useState<string[]>([]);
  const [hoveredGameItemId, setHoveredGameItemId] = useState<string>("");

  const handleHoverLinked = (gameItemId: string) => {
    if (gameItemIdsToShow.includes(gameItemId)) return;
    if (hoveredGameItemId === gameItemId) return;
    setHoveredGameItemId(gameItemId);
  };

  const handleDoneHoveringLinked = (gameItemId: string) => {
    if (gameItemIdsToShow.includes(gameItemId)) return;
    if (hoveredGameItemId !== gameItemId) return;
    setHoveredGameItemId("");
  };

  const handleClickedLinked = (gameItemId: string) => {
    if (gameItemIdsToShow.includes(gameItemId)) {
      setGameItemIdsToShow((idsToShow) =>
        idsToShow.filter((id) => id !== gameItemId)
      );
    } else {
      setGameItemIdsToShow((idsToShow) => [...idsToShow, gameItemId]);
    }
  };

  if (error || plotData == undefined) return;
  const mostCommonCurrencyUsed = plotData.mostCommonCurrencyUsed;
  const mostCommonCurrencyUsedName = capitalizeFirstLetter(
    mostCommonCurrencyUsed ?? ""
  );

  const renderGraph =
    plotData != undefined && mostCommonCurrencyUsed != undefined && !error;

  const fetchedLeagues = plotData.data.map((val) => val.league);

  const isHighlighted = (gameItemId: string) => {
    if (
      gameItemId === hoveredGameItemId ||
      gameItemIdsToShow.includes(gameItemId)
    ) {
      return true;
    }
    return false;
  };
  const getColor = (idx: number) => {
    if (hoveredGameItemId === "" && gameItemIdsToShow.length === 0) {
      return colors[idx];
    }
    return shadedColors[idx];
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
            {/* <Tooltip
              content={
                <CustomTooltip
                  upperBoundry={1000}
                  fetchedLeagues={fetchedLeagues}
                  colors={colors}
                />
              }
              isAnimationActive={false}
            /> */}
            <Legend
              verticalAlign="top"
              height={36}
              payload={plotData.data.map((leagueData, idx) => ({
                id: leagueData.league,
                type: "line",
                value: `${leagueData.league} - ${showChaos ? "Chaos" : mostCommonCurrencyUsedName} value`,
                color: colors[idx],
              }))}
            />
            {showChaos &&
              plotData.data.map(
                (leagueData, idx) =>
                  leagues.includes(leagueData.league) &&
                  leagueData.linkedPrices &&
                  leagueData.linkedPrices.map((linkedPrices) =>
                    isHighlighted(linkedPrices.gameItemId) ? (
                      <Scatter
                        data={linkedPrices.data}
                        dataKey={"valueInChaos"}
                        hide={!showChaos}
                        yAxisId={0}
                        line
                        key={linkedPrices.gameItemId + "_highlighted"}
                        fill={colors[idx]}
                        stroke={"#FFF"}
                        isAnimationActive={false}
                        onMouseOver={() =>
                          handleHoverLinked(linkedPrices.gameItemId)
                        }
                        onMouseOut={() =>
                          handleDoneHoveringLinked(linkedPrices.gameItemId)
                        }
                        onClick={() =>
                          handleClickedLinked(linkedPrices.gameItemId)
                        }
                      />
                    ) : (
                      <Scatter
                        data={linkedPrices.data}
                        dataKey={"valueInChaos"}
                        hide={!showChaos}
                        yAxisId={0}
                        key={linkedPrices.gameItemId + "_highlighted"}
                        fill={getColor(idx)}
                        stroke={getColor(idx)}
                        isAnimationActive={false}
                        onMouseOver={() =>
                          handleHoverLinked(linkedPrices.gameItemId)
                        }
                        onMouseOut={() =>
                          handleDoneHoveringLinked(linkedPrices.gameItemId)
                        }
                        onClick={() =>
                          handleClickedLinked(linkedPrices.gameItemId)
                        }
                      />
                    )
                  )
              )}
            {showChaos &&
              plotData.data.map((leagueData, idx) => {
                return (
                  leagues.includes(leagueData.league) &&
                  leagueData.unlinkedPrices && (
                    <Scatter
                      data={leagueData.unlinkedPrices}
                      dataKey={"valueInChaos"}
                      key={leagueData.league + "_unlinked"}
                      fill={getColor(idx)}
                      stroke={getColor(idx)}
                      yAxisId={0}
                      hide={!showChaos}
                      isAnimationActive={false}
                    />
                  )
                );
              })}
          </ScatterChart>
        </ResponsiveContainer>
      </Box>
    )
  );
}

export default GraphComponent;
