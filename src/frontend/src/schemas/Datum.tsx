/**
 * A single instance of data point containing date, value in chaos and eventually other measures
 */
interface Datum {
  timestamp: number;
  valueInChaos: number;
  valueInMostCommonCurrencyUsed: number;
  confidence: "low" | "medium" | "high";
}

export default Datum;
