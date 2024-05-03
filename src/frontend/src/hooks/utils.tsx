import { ModifierInput } from "../components/Input/ModifierInput";

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

export const capitalizeFirstLetter = (string: string): string => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

export const convertToBoolean = (value: string) => {
  if (value === "true") {
    return true;
  } else if (value === "false") {
    return false;
  } else {
    return undefined;
  }
};

export const delay = (time: number) => {
  return new Promise((resolve) => setTimeout(resolve, time));
};