/**
 * A single instance of data point containing date, value in chaos and eventually other measures
 */
interface Datum {
  date: string;
  valueInChaos: number;
  valueInMostCommonCurrencyUsed: number;
}

export default Datum;
