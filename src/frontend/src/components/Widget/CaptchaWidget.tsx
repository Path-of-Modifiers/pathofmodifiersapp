import Turnstile, { useTurnstile } from "react-turnstile";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

// Cloudfare turnstile widget for captcha
function CaptchaWidget() {
  const turnstile = useTurnstile();
  return (
    <Turnstile
      sitekey={siteKey}
      onVerify={(token) => {
        fetch("/", {
          method: "POST",
          body: JSON.stringify({ token }),
        }).then((response) => {
          if (!response.ok) turnstile.reset();
        });
      }}
    />
  );
}

export default CaptchaWidget;
