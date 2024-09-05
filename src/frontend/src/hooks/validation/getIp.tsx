import { useEffect, useRef } from "react";

/**
 * Get the IP address of the user
 * Gets the IP address of the user and stores it in local storage
 * for use in the captcha validation
 * Hashes the IP address before storing it for 24 hours in DB
 * @returns {string} ip
 */
const useGetIp = () => {
  const ip = useRef<string>("");

  useEffect(() => {
    fetch("https://api.ipify.org?format=json")
      .then((response) => response.json())
      .then((data) => {
        ip.current = data.ip;
        localStorage.setItem("security_ip", ip.current);
      })
      .catch((error) => {
        console.log("Captcha Error fetching IP:", error);
      });
  }, []);

  return ip.current;
};

export default useGetIp;
