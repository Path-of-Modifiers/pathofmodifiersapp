import { Stat, StatProps, StatNumber, StatHelpText } from "@chakra-ui/react";

import {
  getHoursSinceLaunch,
  formatHoursSinceLaunch,
  LEAGUE_LAUNCH_DATETIME,
} from "../../hooks/graphing/utils";
import { DEFAULT_LEAGUE } from "../../config";

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

  const currentTime = new Date();
  const currentDay = currentTime.getDate();
  const currentMonth = currentTime.toLocaleString("default", {
    month: "short",
  });

  console.log(leagueLaunchMonth);

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
