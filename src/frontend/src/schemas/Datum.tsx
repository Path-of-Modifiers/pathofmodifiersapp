/**
 * A single instance of data point containing date, value in chaos and eventually other measures
 */
type Datum = {
  hoursSinceLaunch: number;
  valueInChaos: number | null;
  valueInMostCommonCurrencyUsed: number | null;
  confidence: "low" | "medium" | "high" | null;
}

type TimeseriesData = {
  name: string;
  data: Array<Datum>;
  confidenceRating: 'low' | 'medium' | 'high';
};

export type FilledPlotData = {
  mostCommonCurrencyUsed: string;
  data: Array<TimeseriesData>;
};
