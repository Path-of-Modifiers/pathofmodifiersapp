import { ModifierInput } from "../components/Input/ModifierInputComp/ModifierInput";

// Check if an array is null or contains only null values
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

// Capitalize the first letter of a string
export const capitalizeFirstLetter = (string: string): string => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

// Convert a string to a boolean
export const convertToBoolean = (value: string) => {
  if (value === "true") {
    return true;
  } else if (value === "false") {
    return false;
  } else {
    return undefined;
  }
};

// Convert a boolean to a string
export const delay = (time: number) => {
  return new Promise((resolve) => setTimeout(resolve, time));
};
