/**
 * A single instance of data point containing date, value in chaos and eventually other measures
 */
interface Datum {
    timestamp: string;
    valueInChaos: number;
    valueInMostCommonCurrencyUsed: number;
}

export default Datum;
