import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import testAPI from '../../hooks/graphing/processPlottingData';

interface Datum {
    xaxis: Date | string,
    yaxis1: number,
    yaxis2?: number
}

interface GraphProps {
    data: Datum[]
}

function GraphComponent () {
  const data: Datum[] = testAPI()
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
          <XAxis dataKey="xaxis" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="yaxis1" stroke="#8884d8" />
          {/* {data[0].yaxis2 !== undefined && <Line type="monotone" dataKey="yaxis2" stroke="#82ca9d" />} */}
        </LineChart>
      </ResponsiveContainer>
    );
}

export default GraphComponent;