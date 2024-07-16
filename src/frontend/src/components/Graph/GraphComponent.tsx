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
import { Center, Spinner } from "@chakra-ui/react";
import GetPlotData from "../../hooks/graphing/processPlottingData";
import { useGraphInputStore } from "../../store/GraphInputStore";

/**
 * Uses the globally stored plotQuery state to send a request,
 * the response is processed. Returns a spinner while retrieving
 * data. If no plotQuery has been set, no graph is returned.
 * @returns A spinner while loading data, nothing if no query yet
 * and a graph if there has been
 */
function GraphComponent() {
  const plotQuery = useGraphInputStore((state) => state.plotQuery);
  const { result, fetchStatus } = GetPlotData(plotQuery);

  if (fetchStatus === "fetching") {
    return (
      <Center>
        <Spinner size="xl" color={"ui.white"} />
      </Center>
    );
  }

  return (
    result && (
      <ResponsiveContainer width="100%" height="100%">
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
          <YAxis />
          <Tooltip />
          <Legend verticalAlign="top" height={36} />
          <Line type="monotone" dataKey="valueInChaos" stroke="#8884d8" />
          {/**
           * Example for adding more graphs
           * result[0].yaxis2 !== undefined && <Line type="monotone" dataKey="yaxis2" stroke="#82ca9d" />}
           */}
        </LineChart>
      </ResponsiveContainer>
    )
  );
}

export default GraphComponent;
