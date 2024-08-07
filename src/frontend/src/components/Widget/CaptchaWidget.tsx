import { Turnstile } from "@marsidev/react-turnstile";
import useTurnstileValidation from "../../hooks/turnstile/turnstileValidation";
import { useEffect, useRef, useState } from "react";
import { useTurnstileStore } from "../../store/TurnstileStore";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

// Cloudfare turnstile widget for captcha
const CaptchaWidget = () => {
  const ip = useRef<string>("");
  const [token, setToken] = useState<string>("");
  const { setTurnstileResponse } = useTurnstileStore();
  const { turnstileResponse } = useTurnstileValidation({
    token: token,
    ip: ip.current,
  });

  useEffect(() => {
    fetch("https://api.ipify.org?format=json")
      .then((response) => response.json())
      .then((data) => {
        ip.current = data.ip;
      })
      .catch((error) => {
        console.log("Captcha Error fetching IP:", error);
      });

    if (turnstileResponse) {
      setTurnstileResponse(turnstileResponse);
    }
  }, [turnstileResponse, setTurnstileResponse]);

  return <Turnstile siteKey={siteKey} onSuccess={setToken} />;
};

export default CaptchaWidget;
