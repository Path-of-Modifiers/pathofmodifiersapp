/**
 *
 * @returns
 */
const useGetIp = () => {
  let ip: string | undefined = undefined;

  fetch("https://api.ipify.org?format=json")
    .then((response) => response.json())
    .then((data) => {
      ip = data.ip;
    })
    .catch((error) => {
      console.log("Error fetching IP:", error);
    });
    console.log("IPPPPPPPP", ip);

  if (ip) {
    console.log("YESSSIPPPPPP", ip);
    localStorage.setItem("secured_ip", JSON.stringify(ip));
    return ip;
  }
};

export default useGetIp;
