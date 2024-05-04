import { AxisOptions, Chart } from 'react-charts';
import {useMemo} from "react";
 
type MyDatum = { primary: string, likes: number };

const data = [
    {
      label: 'Series 1',
      data: [
        {
          primary: '2022-02-03T00:00:00.000Z',
          likes: 130,
        },
        {
          primary: '2022-03-03T00:00:00.000Z',
          likes: 150,
        },
      ],
    },
    {
      label: 'Series 2',
      data: [
        {
          primary: '2022-04-03T00:00:00.000Z',
          likes: 200,
        },
        {
          primary: '2022-05-03T00:00:00.000Z',
          likes: 250,
        },
      ],
    },
  ]
 
function MyChart() {
    

    const primaryAxis = useMemo(
        (): AxisOptions<MyDatum> => ({
        getValue: datum => datum.primary,
        }),
        []
    )

    const secondaryAxes = useMemo(
        (): AxisOptions<MyDatum>[] => [
        {
            getValue: datum => datum.likes,
            elementType: "line",
        },
        ],
        []
    )

    return (
        <Chart
        options={{
            data,
            primaryAxis,
            secondaryAxes,
        }}
        />
    )
}

export default MyChart;