import _ from "lodash";

interface meanOfValuesKWARGS {
    topN: number,
    normalValuesOnly: boolean,
    nStandardDeviations: number
}

// Takes in values and optional kwargs
// If kwargs are given, it returns the mean of the topN values that are within nStandardDeviations
// Else it returns the mean of values
function meanOfValues(values: number[], kwargs?: meanOfValuesKWARGS): number {
    if (values.length === 0) {
        return NaN
    }
    if (kwargs !== undefined) {
        const topN = values.length>kwargs.topN?kwargs.topN:values.length;
        values = values.sort(((a, b) => (a - b))).slice(0, topN);
        const normalValues = valuesWithinNStandardDeviations(values, kwargs.nStandardDeviations);
        return normalValues.reduce((acc, val) => acc + val, 0) / normalValues.length;
    } else {
        return values.reduce((acc, val) => acc + val, 0) / values.length
    }
};

// Calculates the standard deviation of values
export const standardDeviation = (values: number[]) => {
    const N = values.length;
    const mean = meanOfValues(values);
    const std = Math.sqrt(
        values
            .reduce((acc, val) => acc.concat((val - mean) ** 2), [] as number[])
            .reduce((acc, val) => acc + val, 0) /
            N
    );
    return std;
};

// Returns values that are within N standard deviations
const valuesWithinNStandardDeviations = (values: number[], N: number) => {

    const mean = meanOfValues(values);
    const std = standardDeviation(values);

    // console.log("mean: ", mean, "std: ", std);
    // console.log("values: ", values);

    const normalValues = values.filter((value) => (Math.abs(value - mean) < N*std));
    // console.log("normal values: ", normalValues);

    return normalValues;
};

interface Datum {
    date: string,
    valueInChaos: number,
    yaxis2?: number
}

// Groups by hour and returns mean of topN values that are within 2 standard deviations
// The returned grouped values have the type of an array of Datums
export const groupByAndMeanTopN = (values: Datum[], topN: number) => {
    const grouped_values: Datum[] = _(values)
        .groupBy(datum => datum.date.toLocaleString().split(":")[0])
        .map(
            (value, key) => (
                {
                    date: key.toLocaleString().split(":")[0], 
                    valueInChaos: meanOfValues(_.map(value, "valueInChaos"), {topN: topN, normalValuesOnly: true, nStandardDeviations: 2})
                }
            )
        )
        .value()
        .slice(0, -1);
    
    return grouped_values;
};