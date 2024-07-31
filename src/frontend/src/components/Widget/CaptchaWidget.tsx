import { Turnstile } from "@marsidev/react-turnstile";
import Cookies from "js-cookie";

// Cloudflare Captcha Widget
export const CaptchaWidget = () => {
  return (
    <Turnstile
      siteKey="0x4AAAAAAAgHwIJ8mwbZ2cuJ"
      onError={() =>
        Cookies.set("cf-captcha-status", "error", {
          expires: 1,
          secure: true,
          sameSite: "strict",
        })
      }
      onExpire={() =>
        Cookies.set("cf-captcha-status", "expired", {
          expires: 1,
          secure: true,
          sameSite: "strict",
        })
      }
      onSuccess={() =>
        Cookies.set("cf-captcha-status", "solved", {
          expires: 1,
          secure: true,
          sameSite: "strict",
        })
      }
    />
  );
};

export default CaptchaWidget;
