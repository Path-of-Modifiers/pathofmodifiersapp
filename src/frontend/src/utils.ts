import type { ApiError } from "./client";
import { Toast } from "./hooks/useCustomToast";

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
