import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "./StandardLayoutInput/SelectBoxInput";
import { CURRENT_SOFTCORE_LEAGUE, CURRENT_HARDCORE_LEAGUE } from "../../config";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  const { league, setLeague } = useGraphInputStore();
  const defaultLeague = CURRENT_SOFTCORE_LEAGUE;
  const defaultHardcoreLeague = CURRENT_HARDCORE_LEAGUE;
  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleLeagueChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      setLeague(newValue.label || CURRENT_SOFTCORE_LEAGUE);
    }
  };

  useEffect(() => {
    if (clearClicked) {
      useGraphInputStore.setState({ league: defaultLeague });
    }
  }, [clearClicked, defaultLeague]);

  const selectLeagueOptions: Array<SelectBoxOptionValue> = [
    { value: defaultLeague, label: defaultLeague, regex: defaultLeague },
    { value: defaultHardcoreLeague, label: defaultHardcoreLeague, regex: defaultHardcoreLeague }
    /* FUTURE IMPLEMENTATION: Add more leagues here */
    // ,
    // ,
    // { value: "Standard", label: "Standard" },
    // ,
    // { value: "Hardcore", label: "Hardcore" },
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
