/**
 * A single instance of data point containing date, value in chaos and eventually other measures
 */
interface Datum {
  timestamp: number;
  valueInChaos: number | null;
  valueInMostCommonCurrencyUsed: number | null;
  confidence: "low" | "medium" | "high" | null;
}

export default Datum;
