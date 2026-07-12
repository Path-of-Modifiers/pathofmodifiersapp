import { Stat, StatProps, StatNumber, StatHelpText } from "@chakra-ui/react";
import { useEffect, useState } from "react";

import {
  getHoursSinceLaunch,
  formatHoursSinceLaunch,
} from "../../hooks/graphing/utils";
import { setupHourlyUpdate } from "../../utils";
import { useLeagueLaunchStats } from "../../store/LeagueLaunchStatsStore";

const DateDaysHoursSinceLaunchStats = (props: StatProps) => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const { league, leagueLaunch, hoursSinceLaunch, setHoursSinceLaunch } =
    useLeagueLaunchStats();
  useEffect(() => {
    return setupHourlyUpdate(setCurrentTime);
  }, []);

  const leagueLaunchDay = leagueLaunch.getDate();
  const leagueLaunchMonth = leagueLaunch.toLocaleString("default", {
    month: "short",
  });
  const leagueLaunchYear = leagueLaunch.toLocaleString("default", {
    year: "numeric",
  });

  const currentDay = currentTime.getDate();
  const currentMonth = currentTime.toLocaleString("default", {
    month: "short",
  });
  const currentYear = currentTime.toLocaleString("default", {
    year: "numeric",
  });

  const curHoursSinceLaunch = getHoursSinceLaunch(currentTime, leagueLaunch);
  const [localHoursSinceLaunch, setLocalHoursSinceLaunch] =
    useState(curHoursSinceLaunch);
  useEffect(() => {
    console.log(currentTime, leagueLaunch);
    const curHoursSinceLaunch = getHoursSinceLaunch(currentTime, leagueLaunch);
    setLocalHoursSinceLaunch(hoursSinceLaunch);
    if (curHoursSinceLaunch !== hoursSinceLaunch) {
      setHoursSinceLaunch(curHoursSinceLaunch);
    }
  }, [
    leagueLaunch,
    hoursSinceLaunch,
    setHoursSinceLaunch,
    currentTime,
    localHoursSinceLaunch,
  ]);

  const daysHoursSinceLaunchFormat = formatHoursSinceLaunch(
    localHoursSinceLaunch,
  );
  const [yearsDays, sinceLaunchHours] = daysHoursSinceLaunchFormat.split("T");
  const [sinceLaunchYears, sinceLaunchDays] = yearsDays.split("Y");

  return (
    <Stat {...props}>
      <StatNumber>
        {sinceLaunchYears !== "0" ? `${sinceLaunchYears} years, ` : ""}
        {sinceLaunchDays} days and {sinceLaunchHours} hours since {league.name}{" "}
        launched
      </StatNumber>
      <StatHelpText>
        {leagueLaunchMonth} {leagueLaunchDay} {leagueLaunchYear} -{" "}
        {currentMonth} {currentDay} {currentYear}
      </StatHelpText>
    </Stat>
  );
};

export default DateDaysHoursSinceLaunchStats;
