import _ from "lodash";

interface meanOfValuesKWARGS {
    normalValuesOnly: boolean,
    nStandardDeviations: number
}

function meanOfValues(values: number[], kwargs?: meanOfValuesKWARGS): number {
    if (values.length === 0) {
        return NaN
    }
    if (kwargs !== undefined) {
        const normalValues = valuesWithinNStandardDeviations(values, kwargs.nStandardDeviations);
        return normalValues.reduce((acc, val) => acc + val, 0) / normalValues.length;
    } else {
        return values.reduce((acc, val) => acc + val, 0) / values.length
    }
};

export const standardDeviation = (values: number[]) => {
    const N = values.length;
    const mean = meanOfValues(values);
    const std = Math.sqrt(
        values
            .reduce((acc, val) => acc.concat((val - mean) ** 2), [])
            .reduce((acc, val) => acc + val, 0) /
            N
    );
    return std;
};

const valuesWithinNStandardDeviations = (values: number[], N: number) => {
    const topN = values.length>20?20:values.length;
    values = values.sort(((a, b) => (a - b))).slice(0, topN);

    const mean = meanOfValues(values);
    const std = standardDeviation(values);

    // console.log("mean: ", mean, "std: ", std);
    // console.log("values: ", values);

    const normalValues = values.filter((value) => (Math.abs(value - mean) < N*std));
    // console.log("normal values: ", normalValues);

    return normalValues;
}

const meanOfTopN = (values: number[], topN: number) => {
    const valuesTopN = values.sort(((a, b) => (a - b))).slice(0, topN);
    const meanTopN = meanOfValues(valuesTopN)

    return meanTopN;
};


interface Datum {
    date: string,
    valueInChaos: number,
    yaxis2?: number
}

export const groupByAndMeanTopN = (values: Datum[], topN: number) => {
    const grouped_values = _(values)
        .groupBy(datum => datum.date.toLocaleString().split(":")[0])
        .map(
            (value, key) => (
                {
                    date: key.toLocaleString().split(":")[0], 
                    // valueInChaos: meanOfTopN(_.map(value, "valueInChaos"), topN)
                    valueInChaos: meanOfValues(_.map(value, "valueInChaos"), {normalValuesOnly: true, nStandardDeviations: 2})
                }
            )
        )
        .value()
        .slice(0, -1);
    
    return grouped_values;
};