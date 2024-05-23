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
import getPlotData from "../../hooks/graphing/processPlottingData";
import Datum from "../../schemas/Datum";

function GraphComponent() {
  const data: Datum[] = getPlotData();
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        width={500}
        height={300}
        data={data}
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
         * data[0].yaxis2 !== undefined && <Line type="monotone" dataKey="yaxis2" stroke="#82ca9d" />}
         */}
      </LineChart>
    </ResponsiveContainer>
  );
}

export default GraphComponent;
