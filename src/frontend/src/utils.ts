import type { ApiError } from "./client";
import { Toast } from "./hooks/useCustomToast";
import { DEFAULT_LEAGUES } from "./config";
import { useGraphInputStore } from "./store/GraphInputStore";

export const emailPattern = {
  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
  message: "Invalid email address",
};

export const usernamePattern = {
  value: /^[\p{L}0-9_]+$/u,
  message: "Invalid username",
};

interface PasswordRules {
  password?: string;
  new_password?: string;
  minLength?: {
    value: number;
    message: string;
  };
  required?: string;
  validate?: (value: string) => boolean | string;
}

export const passwordRules = (isRequired = true) => {
  const rules: PasswordRules = {
    minLength: {
      value: 8,
      message: "Password must be at least 8 characters",
    },
  };

  if (isRequired) {
    rules.required = "Password is required";
  }

  return rules;
};

export const confirmPasswordRules = (
  getValues: () => PasswordRules,
  isRequired = true,
) => {
  const rules: PasswordRules = {
    validate: (value: string) => {
      const password = getValues().password || getValues().new_password;
      return value === password ? true : "The passwords do not match";
    },
  };

  if (isRequired) {
    rules.required = "Password confirmation is required";
  }

  return rules;
};

export const handleError = (err: ApiError, showToast: Toast) => {
  const errDetail = err.body?.detail;
  let errorMessage = errDetail || "Something went wrong.";
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    errorMessage = errDetail[0].msg;
  }
  showToast("Error", errorMessage, "error");
};

export function msToNextHour() {
  return 3600000 - (new Date().getTime() % 3600000);
}

type SetDateFunction = (date: Date) => void;

export const setupHourlyUpdate = (setCurrentTime: SetDateFunction) => {
  let timeoutId: NodeJS.Timeout;

  const updateTime = () => {
    setCurrentTime(new Date());
    timeoutId = setTimeout(updateTime, msToNextHour()); // Recalculate delay
  };

  timeoutId = setTimeout(updateTime, msToNextHour());

  return () => clearTimeout(timeoutId);
};

const validateLeagues = (searchParams: URLSearchParams) => {
  const leagues = searchParams.get("league");
  if (searchParams.size === 1 && leagues) {
    if (leagues.length > 1 || !leagues.includes(DEFAULT_LEAGUES[0])) {
      throw "default league not in simple url";
    }
  } else if (!leagues || leagues.length === 0) {
    throw "leagues not set in url";
  }
};

export const validateAndSetSearchParams = (searchParams: URLSearchParams) => {
  try {
    validateLeagues(searchParams);
  } catch (error) {
    const graphState = useGraphInputStore.getState();
    graphState.removeAllLeagues();
    graphState.addLeague(DEFAULT_LEAGUES[0]);
    const searchParams = new URLSearchParams();
    searchParams.set("league", DEFAULT_LEAGUES[0]);
    location.hash = searchParams.toString();
  }
};
