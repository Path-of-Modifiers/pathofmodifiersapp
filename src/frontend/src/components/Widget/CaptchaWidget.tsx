import { Turnstile } from "@marsidev/react-turnstile";
import Cookies from "js-cookie";

// Cloudfare Captcha Widget
export const CaptchaWidget = () => {
  return (
    <Turnstile
      siteKey="0x4AAAAAAAgHwIJ8mwbZ2cuJ"
      // Set cookies variables for 24 hours to track captcha status
      onError={() => Cookies.set("cf-captcha-status", "error")}
      onExpire={() => Cookies.set("cf-captcha-status", "expired")}
      onSuccess={() =>
        Cookies.set("cf-captcha-status", "solved", { expires: 1 })
      }
    />
  );
};

export default CaptchaWidget;
