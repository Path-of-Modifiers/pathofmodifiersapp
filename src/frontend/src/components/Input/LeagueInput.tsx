import { useGraphInputStore } from "../../store/GraphInputStore";
import { useLeagueLaunchStats } from "../../store/LeagueLaunchStatsStore";
import MultiSelectButtonGrid from "../Common/MultiSelectButtonGrid";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  const { league } = useLeagueLaunchStats();
  const { leagues, choosableLeagues, addLeague, removeLeague } =
    useGraphInputStore();

  const selectLeagueOptions: string[] = choosableLeagues.map(
    (league) => league.name,
  );
  let defaultLeagues;
  if (leagues.length > 0) {
    defaultLeagues = leagues;
  } else {
    defaultLeagues = league ? [league.name] : undefined;
  }
  return (
    <MultiSelectButtonGrid
      optionsName="Select one or more Leagues"
      options={selectLeagueOptions}
      defaultSelectedOptions={defaultLeagues}
      setValue={addLeague}
      removeValue={removeLeague}
      onClearClick={() =>
        useGraphInputStore.setState({ leagues: defaultLeagues })
      }
    />
  );
};
