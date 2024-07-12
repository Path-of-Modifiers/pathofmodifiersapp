import { useErrorStore } from "../../store/ErrorStore";
import { useGraphInputStore } from "../../store/GraphInputStore";

const { setLeagueError, setModifiersError } = useErrorStore.getState();

const plotQueryStore = useGraphInputStore.getState().plotQuery;

/**
 * Checks whether the League input for the graph query is valid
 * @returns boolean
 */
export const checkGraphQueryLeageInput = () => {
  // If league is empty, return false
  console.log("LEAGUE CHECKED");
  if (plotQueryStore.league === "") {
    setLeagueError(true);
    return false;
  }
  setLeagueError(false);
  return true;
};

/**
 * Checks whether the modifiers input for the graph query is valid
 * @returns boolean
 */
export const checkGraphQueryModifierInput = () => {
  console.log("MODIFIER CHECKED");
  // If modifiers are empty, return false
  if (plotQueryStore.wantedModifiers.length === 0) {
    setModifiersError(true);
    return false;
  }
  setModifiersError(false);
  return true;
};
