import { Turnstile } from "@marsidev/react-turnstile";
import { useState } from "react";
import { Text } from "@chakra-ui/react";
import useTurnstileValidation from "../../hooks/validation/turnstileValidation";
import useGetIp from "../../hooks/validation/getIp";

const siteKey = import.meta.env.VITE_APP_TURNSTILE_SITE_KEY || "";

// Cloudfare turnstile widget for captcha
const CaptchaWidget = () => {
  const [token, setToken] = useState<string>("");
  const security_ip = useGetIp();

  const { performTurnstileValidation, error, resetError } =
    useTurnstileValidation({
      token: token,
      ip: security_ip,
    });

  const turnstileHandler = async (token: string) => {
    setToken(token);
    resetError();

    try {
      await performTurnstileValidation.mutateAsync({
        token: token,
        ip: security_ip,
      });
    } catch {
      // error is handled by useAuth hook
    }
  };

  return (
    <>
      {!error && <Turnstile siteKey={siteKey} onSuccess={turnstileHandler} />}
      {error && <Text color={"ui.white"}>{error}</Text>}
    </>
  );
};

export default CaptchaWidget;
