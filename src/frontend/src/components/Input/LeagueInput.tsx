import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
  HandleChangeEventFunction,
} from "./StandardLayoutInput/SelectBoxInput";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  // FUTURE IMPLEMENTATION: Add default hardcore league
  //   const defaultHardcoreLeague = import.meta.env.CURRENT_HARDCORE_LEAGUE;
  const { setLeague } = useGraphInputStore();

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const defaultLeague = import.meta.env.VITE_APP_DEFAULT_LEAGUE || "";

  const handleLeagueChange: HandleChangeEventFunction = (newValue) => {
    if (newValue) {
      setLeague(newValue.label || defaultLeague);
    }
  };

  useEffect(() => {
    useGraphInputStore.setState({ league: defaultLeague });

    if (clearClicked) {
      useGraphInputStore.setState({ league: defaultLeague });
    }
  }, [clearClicked, defaultLeague]);

  const selectLeagueOptions: Array<SelectBoxOptionValue> = [
    { value: defaultLeague, label: defaultLeague, regex: defaultLeague },
    /* FUTURE IMPLEMENTATION: Add more leagues here */
    // ,
    // { value: defaultHardcoreLeague, text: defaultHardcoreLeague },
    // ,
    // { value: "Standard", text: "Standard" },
    // ,
    // { value: "Hardcore", text: "Hardcore" },
  ];

  return (
    <SelectBoxInput
      optionsList={selectLeagueOptions}
      handleChange={handleLeagueChange}
      descriptionText={"League"}
      defaultText={defaultLeague}
      multipleValues={false}
      id={`leagueInput-0`}
    />
  );
};
