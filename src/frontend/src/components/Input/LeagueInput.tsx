import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "./StandardLayoutInput/SelectBoxInput";
import { DEFAULT_LEAGUE } from "../../config";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  // FUTURE IMPLEMENTATION: Add default hardcore league
  //   const defaultHardcoreLeague = import.meta.env.CURRENT_HARDCORE_LEAGUE;
  const { league, setLeague } = useGraphInputStore();
  const defaultLeague = DEFAULT_LEAGUE;
  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleLeagueChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      setLeague(newValue.label || DEFAULT_LEAGUE);
    }
  };

  useEffect(() => {
    if (clearClicked) {
      useGraphInputStore.setState({ league: defaultLeague });
    }
  }, [clearClicked, defaultLeague]);

  const selectLeagueOptions: Array<SelectBoxOptionValue> = [
    { value: defaultLeague, label: defaultLeague, regex: defaultLeague },
    /* FUTURE IMPLEMENTATION: Add more leagues here */
    // ,
    // { value: defaultHardcoreLeague, label: defaultHardcoreLeague },
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
