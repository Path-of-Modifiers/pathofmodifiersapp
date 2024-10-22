// Capitalize the first letter of a string
export const capitalizeFirstLetter = (string: string): string => {
  return string.charAt(0).toUpperCase() + string.slice(1);
};

// Convert a string to a boolean
export const convertToBoolean = (value: string) => {
  if (value === "Yes") {
    return true;
  } else if (value === "No") {
    return false;
  } else {
    return undefined;
  }
};

export const delay = (time: number) => {
  return new Promise((resolve) => setTimeout(resolve, time));
};
