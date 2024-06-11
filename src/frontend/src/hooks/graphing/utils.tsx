import Datum from "../../schemas/Datum";

export function allValueInChaos(
  values: Datum[],
  valueInChaos: number
): Datum[] | undefined {
  if (values.length === 0) {
    return undefined;
  }
  for (const i in values) {
    values[i].valueInChaos = valueInChaos;
  }
  return values;
}
