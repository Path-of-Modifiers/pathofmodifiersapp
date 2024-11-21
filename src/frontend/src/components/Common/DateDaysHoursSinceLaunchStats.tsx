import { Stat, StatProps, StatNumber, StatHelpText } from "@chakra-ui/react";
import { useEffect, useState } from "react";

import {
  getHoursSinceLaunch,
  formatHoursSinceLaunch,
  LEAGUE_LAUNCH_DATETIME,
} from "../../hooks/graphing/utils";
import { DEFAULT_LEAGUE } from "../../config";
import { msToNextHour } from "../../utils";

const DateDaysHoursSinceLaunchStats = (props: StatProps) => {
  const defaultLeague = DEFAULT_LEAGUE;
  const hoursSinceLaunch = getHoursSinceLaunch();
  const daysHoursSinceLaunchFormat = formatHoursSinceLaunch(hoursSinceLaunch);
  const [sinceLaunchDays, sinceLaunchHours] =
    daysHoursSinceLaunchFormat.split("T");

  const leagueLaunchDay = LEAGUE_LAUNCH_DATETIME.getDate();
  const leagueLaunchMonth = LEAGUE_LAUNCH_DATETIME.toLocaleString("default", {
    month: "short",
  });

  const [currentTime, setCurrentTime] = useState(new Date());
  const currentDay = currentTime.getDate();
  const currentMonth = currentTime.toLocaleString("default", {
    month: "short",
  });

  useEffect(() => {
    const updateWaitTime = msToNextHour();
    const intervalId = setInterval(() => {
      setCurrentTime(new Date());
    }, updateWaitTime);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <Stat {...props}>
      <StatNumber>
        {sinceLaunchDays} days and {sinceLaunchHours} hours since{" "}
        {defaultLeague} launched
      </StatNumber>
      <StatHelpText>
        {leagueLaunchMonth} {leagueLaunchDay} - {currentMonth} {currentDay}
      </StatHelpText>
    </Stat>
  );
};

export default DateDaysHoursSinceLaunchStats;
