import { Turnstile } from "@marsidev/react-turnstile";
import useTurnstileValidation from "../../hooks/validation/turnstileValidation";
import { useState } from "react";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

// Cloudfare turnstile widget for captcha
const CaptchaWidget = () => {
  const [token, setToken] = useState<string>("");
  const security_ip = localStorage.getItem("security_ip");

  useTurnstileValidation({
    token: token,
    ip: security_ip ?? "",
  });

  return <Turnstile siteKey={siteKey} onSuccess={setToken} />;
};

export default CaptchaWidget;
