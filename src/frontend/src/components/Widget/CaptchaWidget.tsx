import Turnstile, { useTurnstile } from "react-turnstile";
import useTurnstileValidation from "../../hooks/turnstile/turnstileValidation";
import { useEffect, useRef, useState } from "react";
import { TurnstileResponse } from "../../client";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

interface CaptchaWidgetProps {
  onTurnstileResponse: (response: TurnstileResponse | undefined) => void;
}

// Cloudfare turnstile widget for captcha
const CaptchaWidget = (props: CaptchaWidgetProps) => {
  const ip = useRef<string>("");
  const [token, setToken] = useState<string>("");
  const { turnstileResponse } = useTurnstileValidation({
    token: token,
    ip: ip.current,
  });
  const turnstile = useTurnstile();

  useEffect(() => {
    fetch("https://api.ipify.org?format=json")
      .then((response) => response.json())
      .then((data) => {
        ip.current = data.ip;
      })
      .catch((error) => {
        console.log("Captcha Error fetching IP:", error);
      });
  }, []);

  useEffect(() => {
    if (!turnstileResponse || !turnstileResponse.success) {
      turnstile.reset();
    }
    props.onTurnstileResponse?.(turnstileResponse ?? undefined);
  }, [turnstile, turnstileResponse, props]);

  return (
    <Turnstile
      sitekey={siteKey}
      onVerify={(token) => {
        setToken(token);
      }}
    />
  );
};

export default CaptchaWidget;
