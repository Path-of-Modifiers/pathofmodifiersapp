import { ModifierInput } from "../components/Graph/ModifierInput";



export const isArrayNullOrContainsOnlyNull = (
    arr:
      | Array<ModifierInput | string | number | null | boolean>
      | null
      | undefined
  ): boolean => {
    if (arr === null || arr === undefined) {
      return true; // If the array is null, return true
    }
    // Check if every element in the array is null
    return arr.every((value) => value === null);
  };