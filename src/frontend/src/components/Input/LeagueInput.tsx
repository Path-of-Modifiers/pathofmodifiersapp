import { useGraphInputStore } from "../../store/GraphInputStore";
import { DEFAULT_LEAGUES, ADDITIONAL_LEAGUES } from "../../config";
import MultiSelectButtonGrid from "../Common/MultiSelectButtonGrid";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  const { leagues, addLeague, removeLeague } = useGraphInputStore();
  // const clearClicked = useGraphInputStore((state) => state.clearClicked);
  console.log(leagues);
  // const handleLeagueChange: HandleChangeEventFunction = (newValue) => {
  //   if (newValue) {
  //     setLeague(newValue.label || DEFAULT_LEAGUE);
  //   }
  // };

  // useEffect(() => {
  //   if (clearClicked) {
  //     useGraphInputStore.setState({ leagues: [DEFAULT_LEAGUE] });
  //   }
  // }, [clearClicked]);

  const selectLeagueOptions: string[] = [...DEFAULT_LEAGUES, ...ADDITIONAL_LEAGUES]
  // const selectLeagueOptions: Array<SelectBoxOptionValue> = [
  //   { value: DEFAULT_LEAGUE, label: DEFAULT_LEAGUE, regex: DEFAULT_LEAGUE },
  //   ...ADDITIONAL_LEAGUES.map((league) => ({ value: league, label: league, regex: league }))
  // ];
  return (
    <MultiSelectButtonGrid
      optionsName="Leagues"
      options={selectLeagueOptions}
      defaultSelectedOptions={leagues}
      setValue={addLeague}
      removeValue={removeLeague}
      onClearClick={() => useGraphInputStore.setState({ leagues: DEFAULT_LEAGUES })}
    />
  )
};
