import { useGraphInputStore } from "../../store/GraphInputStore";
import { DEFAULT_LEAGUES, ADDITIONAL_LEAGUES } from "../../config";
import MultiSelectButtonGrid from "../Common/MultiSelectButtonGrid";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  const { leagues, addLeague, removeLeague } = useGraphInputStore();


  const selectLeagueOptions: string[] = [...DEFAULT_LEAGUES, ...ADDITIONAL_LEAGUES]

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
