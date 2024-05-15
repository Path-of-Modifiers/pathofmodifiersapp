import { Flex, Select, Text } from "@chakra-ui/react";
import { useGraphInputStore } from "../../store/GraphInputStore";
import { useEffect } from "react";

// League Input Component  -  This component is used to select the league of the game.
export const LeagueInput = () => {
  // Needs to be updated to reflect the defualt leagues available in the game
  const defaultLeague = "Necropolis";
  // FUTURE IMPLEMENTATION: Add default hardcore league
  //   const defaultHardcoreLeague = process.env.CURRENT_HARDCORE_LEAGUE;

  const clearClicked = useGraphInputStore((state) => state.clearClicked);

  const handleLeagueChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const league = event.target.value;
    useGraphInputStore.setState({ league: league });
  };

  useEffect(() => {
    useGraphInputStore.setState({ league: defaultLeague });

    if (clearClicked) {
      useGraphInputStore.setState({ league: defaultLeague });
    }
  }, [defaultLeague, clearClicked]);

  return (
    <Flex
      alignItems={"center"}
      color={"ui.white"}
      bgColor={"ui.secondary"}
      m={1}
    >
      <Text ml={1} width={150}>
        League
      </Text>
      <Select
        bgColor={"ui.input"}
        color={"ui.white"}
        defaultValue={"Unique"}
        onChange={(e) => handleLeagueChange(e)}
        width={150}
        focusBorderColor={"ui.white"}
        borderColor={"ui.grey"}
        mr={1}
        ml={1}
        key={"ItemRarityInput"}
      >
        {
          <option
            value={defaultLeague}
            key={"league" + "_option_" + "necropolis"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            {defaultLeague}
          </option>
        }

        {/* FUTURE IMPLEMENTATION: Add more leagues here */}

        {/* ,
        {
          <option
            value={defaultHardcoreLeague}
            key={"league" + "_option_" + "necropolis_hardcore"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            {defaultHardcoreLeague}
          </option>
        }
        ,
        {
          <option
            value={"Standard"}
            key={"league" + "_option_" + "standard"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            Standard
          </option>
        }
        ,
        {
          <option
            value={"Hardcore"}
            key={"league" + "_option_" + "hardcore"}
            style={{ color: "white", backgroundColor: "#2d3333" }}
          >
            Hardcore
          </option>
        } */}
      </Select>
    </Flex>
  );
};
