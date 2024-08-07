import { Turnstile } from "@marsidev/react-turnstile";
import useTurnstileValidation from "../../hooks/turnstile/turnstileValidation";
import { useEffect, useRef, useState } from "react";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

// Cloudfare turnstile widget for captcha
const CaptchaWidget = () => {
  const ip = useRef<string>("");
  const [token, setToken] = useState<string>("");
  useTurnstileValidation({
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
  }, []);

  return <Turnstile siteKey={siteKey} onSuccess={setToken} />;
};

export default CaptchaWidget;
