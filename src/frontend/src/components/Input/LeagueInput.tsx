import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";
import { defaultLeague } from "../../env-vars";
import {
  SelectBox,
  SelectBoxOptionValue,
} from "./StandardLayoutInput/SelectBoxInput";

// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  // FUTURE IMPLEMENTATION: Add default hardcore league
  //   const defaultHardcoreLeague = process.env.CURRENT_HARDCORE_LEAGUE;

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const currentLeagueSelected = useGraphInputStore((state) => state.league);

  const handleLeagueChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const league = event.target.value;
    useGraphInputStore.setState({ league: league });
  };

  useEffect(() => {
    useGraphInputStore.setState({ league: defaultLeague });

    if (clearClicked) {
      useGraphInputStore.setState({ league: defaultLeague });
    }
  }, [clearClicked]);

  const selectLeagueOptions: Array<SelectBoxOptionValue> = [
    /* FUTURE IMPLEMENTATION: Add more leagues here */
    // ,
    // { value: defaultHardcoreLeague, text: defaultHardcoreLeague },
    // ,
    // { value: "Standard", text: "Standard" },
    // ,
    // { value: "Hardcore", text: "Hardcore" },
  ];

  return (
    <SelectBox
      descriptionText={"League"}
      optionsList={selectLeagueOptions}
      itemKeyId={"LeagueInput"}
      defaultValue={defaultLeague}
      defaultText={defaultLeague}
      handleChange={(e) => handleLeagueChange(e)}
      getSelectValue={() => currentLeagueSelected}
    />
  );
};
