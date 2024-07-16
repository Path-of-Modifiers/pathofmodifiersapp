import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";
import { defaultSoftcoreLeague } from "../../env-vars";
import {
  SelectBoxInput,
  SelectBoxOptionValue,
} from "./StandardLayoutInput/SelectBoxInput";
import { getEventTextContent } from "../../hooks/utils";

// Set the default league in the environment variables file.
// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  // FUTURE IMPLEMENTATION: Add default hardcore league
  //   const defaultHardcoreLeague = process.env.CURRENT_HARDCORE_LEAGUE;
  const { setLeague } = useGraphInputStore();

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleLeagueChange = (
    event: React.FormEvent<HTMLElement> | React.ChangeEvent<HTMLInputElement>
  ) => {
    const league = getEventTextContent(event);
    setLeague(league || defaultSoftcoreLeague);
  };

  const getLeagueValue = () => {
    const league = useGraphInputStore.getState().league;
    if (league) {
      return league;
    } else {
      return "";
    }
  };

  useEffect(() => {
    useGraphInputStore.setState({ league: defaultSoftcoreLeague });

    if (clearClicked) {
      useGraphInputStore.setState({ league: defaultSoftcoreLeague });
    }
  }, [clearClicked]);

  const selectLeagueOptions: Array<SelectBoxOptionValue> = [
    { value: defaultSoftcoreLeague, text: defaultSoftcoreLeague },
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
      descriptionText={"League"}
      optionsList={selectLeagueOptions}
      itemKeyId={"LeagueInput"}
      defaultValue={defaultSoftcoreLeague}
      defaultText={defaultSoftcoreLeague}
      getSelectTextValue={getLeagueValue()}
      handleChange={(e) => handleLeagueChange(e)}
    />
  );
};
