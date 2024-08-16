function formatDateToLocal(date: string): string {
  // Parse the UTC date string
  const utcDate = new Date(date);

  // Get the local time as an offset from UTC
  const localOffset = utcDate.getTimezoneOffset() * 60000; // in milliseconds

  // Convert UTC time to local time by applying the offset
  const localDate = new Date(utcDate.getTime() - localOffset);

  // Format the date as "MMM. DD" (e.g., "Aug. 12")
  const formattedDate = localDate
    .toLocaleDateString("en-GB", { month: "short", day: "numeric" })
    .replace(".", "");

  // Format the time as "kl HHmm" (e.g., "kl 1830")
  const formattedTime = localDate
    .toLocaleTimeString("en-GB", {
      hour: "2-digit",
      hour12: false,
    })
    .replace(":", "");

  // Combine the date and time into the desired format
  return `${formattedDate}T${formattedTime}`;
}

export default formatDateToLocal;
