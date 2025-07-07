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
import { capitalizeFirstLetter } from "../../hooks/utils";
import { CustomTooltip } from "./CustomTooltip";
import {
    formatHoursSinceLaunch,
} from "../../hooks/graphing/utils";
import { BiError } from "react-icons/bi";
import { ErrorMessage } from "../Input/StandardLayoutInput/ErrorMessage";
import useGetPlotData from "../../hooks/graphing/processPlottingData";
import NewPlotCustomizationButtons from "../Common/PlotCustomizationButtons";

/**
 * Uses the globally stored plotQuery state to send a request,
 * the response is processed. Returns a spinner while retrieving
 * data. If no plotQuery has been set, no graph is returned.
 * @returns A spinner while loading data, nothing if no query yet
 * and a graph if there has been
 */
function GraphComponent(props: BoxProps) {
    const { plotQuery, leagues } = useGraphInputStore();
    const { result: plotData,
        mostCommonCurrencyUsed,
        confidenceRating,
        upperBoundryChaos,
        upperBoundrySecondary,
        fetchStatus,
        error } = useGetPlotData(plotQuery);


    const mostCommonCurrencyUsedName = `${capitalizeFirstLetter(mostCommonCurrencyUsed ?? "")} value`;
    const renderGraph =
        plotData != undefined && mostCommonCurrencyUsed != undefined && !error;
    const showChaos = usePlotSettingsStore((state) => state.showChaos);
    const showSecondary = usePlotSettingsStore((state) => state.showSecondary);

    if (error || plotData == undefined) return;
    const fetchedLeagues = plotData.data.map((val) => val.name);

    const isLowConfidence = confidenceRating === "low";
    const isMediumConfidence = confidenceRating === "medium";
    const confidenceColor = isLowConfidence
        ? "ui.lowConfidencePrimary"
        : isMediumConfidence
            ? "ui.mediumConfidencePrimary"
            : "ui.input";

    const colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ]


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
                    <NewPlotCustomizationButtons
                        flexProps={{ justifyContent: "center", mt: "10px" }}
                        mostCommonCurrencyUsed={mostCommonCurrencyUsed}
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
                                value: "Chaos value",
                                angle: -90,
                                position: "insideLeft",
                            }}
                            hide={!showChaos}
                            type="number"
                            dataKey={"valueInChaos"}
                            domain={[0, upperBoundryChaos]}
                            allowDataOverflow
                        />
                        <Tooltip
                            content={<CustomTooltip upperBoundry={upperBoundryChaos} fetchedLeagues={fetchedLeagues} colors={colors} />}
                            isAnimationActive={false}
                        />
                        <Legend verticalAlign="top" height={36} />
                        {plotData.data.map((series, idx) => (
                            leagues.includes(series.name) && (<Line
                                type="monotone"
                                data={series.data}
                                dataKey={"valueInChaos"}
                                key={series.name}
                                name={series.name + " - " + "Chaos Value"}
                                stroke={colors[idx]}
                                yAxisId={0}
                                hide={!showChaos}
                                isAnimationActive={false}
                                dot={{ fill: colors[idx] }}
                                legendType={showChaos ? "line" : "none"}
                            />)
                        ))}
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
                            domain={[0, upperBoundrySecondary]}
                            allowDataOverflow
                        />
                        {mostCommonCurrencyUsed !== "chaos" && plotData.data.map((series, idx) => (
                            leagues.includes(series.name) && (<Line
                                type="monotone"
                                data={series.data}
                                dataKey={"valueInMostCommonCurrencyUsed"}
                                key={series.name}
                                name={series.name + " - " + mostCommonCurrencyUsedName}
                                stroke={colors[idx]}
                                yAxisId={1}
                                hide={!showSecondary}
                                isAnimationActive={false}
                                dot={{ fill: colors[idx] }}
                                legendType={showSecondary ? "line" : "none"}
                            />)
                        ))}
                    </LineChart>
                </ResponsiveContainer>
            </Box>
        )
    );
}

export default GraphComponent;
