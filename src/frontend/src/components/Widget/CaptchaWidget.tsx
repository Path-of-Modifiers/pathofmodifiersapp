import Turnstile, { useTurnstile } from "react-turnstile";
import useTurnstyleValidation from "../../hooks/turnstyle/turnstyleValidation";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

const Verify = (token: string, ip: string) => {
  const { turnstyleResponse, fetchStatus, isFetched, isError } =
    useTurnstyleValidation({
      token: token,
      ip: ip,
    });

  if (isError) {
    return false;
  }
  return { turnstyleResponse, fetchStatus, isFetched, isError };
};

// Cloudfare turnstile widget for captcha
const CaptchaWidget = () => {
  let ip = "";
  fetch("https://api.ipify.org?format=json")
    .then((response) => response.json())
    .then((data) => {
      ip = data.ip;
    })
    .catch((error) => {
      console.log("Error fetching IP:", error);
    });

  const turnstile = useTurnstile();
  return (
    <Turnstile
      sitekey={siteKey}
      onVerify={(token) => {
        if (!Verify(token, ip)) {
          turnstile.reset();
        }
      }}
    />
  );
};

export default CaptchaWidget;
