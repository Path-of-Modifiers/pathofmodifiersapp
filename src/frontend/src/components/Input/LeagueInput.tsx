import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "./StandardLayoutInput/SelectBoxInput";
import { DEFAULT_LEAGUE, ADDITIONAL_LEAGUES } from "../../config";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  const { league, setLeague } = useGraphInputStore();
  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleLeagueChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      setLeague(newValue.label || DEFAULT_LEAGUE);
    }
  };

  useEffect(() => {
    if (clearClicked) {
      useGraphInputStore.setState({ league: DEFAULT_LEAGUE });
    }
  }, [clearClicked]);

  const selectLeagueOptions: Array<SelectBoxOptionValue> = [
    { value: DEFAULT_LEAGUE, label: DEFAULT_LEAGUE, regex: DEFAULT_LEAGUE },
    ...ADDITIONAL_LEAGUES.map((league) => ({ value: league, label: league, regex: league }))
  ];

  return (
    <SelectBoxInput
      optionsList={selectLeagueOptions}
      handleChange={handleLeagueChange}
      descriptionText={"League"}
      defaultText={league}
      multipleValues={false}
      id={`leagueInput-0`}
    />
  );
};
