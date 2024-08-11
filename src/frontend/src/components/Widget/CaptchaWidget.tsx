import { Turnstile } from "@marsidev/react-turnstile";
import useTurnstileValidation from "../../hooks/validation/turnstileValidation";
import { useEffect, useState } from "react";
import { useTurnstileStore } from "../../store/TurnstileStore";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

// Cloudfare turnstile widget for captcha
const CaptchaWidget = () => {
  const [token, setToken] = useState<string>("");
  const { setTurnstileResponse } = useTurnstileStore();
  const security_ip = localStorage.getItem("security_ip");
  const { turnstileResponse } = useTurnstileValidation({
    token: token,
    ip: security_ip ?? "",
  });

  useEffect(() => {
    if (turnstileResponse) {
      setTurnstileResponse(turnstileResponse);
    }
  }, [turnstileResponse, setTurnstileResponse]);

  return <Turnstile siteKey={siteKey} onSuccess={setToken} />;
};

export default CaptchaWidget;
