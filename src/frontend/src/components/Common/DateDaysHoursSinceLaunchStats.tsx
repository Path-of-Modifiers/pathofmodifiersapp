import { Stat, StatProps, StatNumber, StatHelpText } from "@chakra-ui/react";
import { useEffect, useState } from "react";

import {
  getHoursSinceLaunch,
  formatHoursSinceLaunch,
  LEAGUE_LAUNCH_DATETIME,
} from "../../hooks/graphing/utils";
import { DEFAULT_LEAGUES } from "../../config";
import { setupHourlyUpdate } from "../../utils";

const DateDaysHoursSinceLaunchStats = (props: StatProps) => {
  const defaultLeague = DEFAULT_LEAGUES[0];

  const leagueLaunchDay = LEAGUE_LAUNCH_DATETIME.getDate();
  const leagueLaunchMonth = LEAGUE_LAUNCH_DATETIME.toLocaleString("default", {
    month: "short",
  });

  const [currentTime, setCurrentTime] = useState(new Date());
  const currentDay = currentTime.getDate();
  const currentMonth = currentTime.toLocaleString("default", {
    month: "short",
  });

  const hoursSinceLaunch = getHoursSinceLaunch(currentTime);
  const daysHoursSinceLaunchFormat = formatHoursSinceLaunch(hoursSinceLaunch);
  const [sinceLaunchDays, sinceLaunchHours] =
    daysHoursSinceLaunchFormat.split("T");

  useEffect(() => {
    return setupHourlyUpdate(setCurrentTime);
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
