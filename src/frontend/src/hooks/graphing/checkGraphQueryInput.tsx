import { useErrorStore } from "../../store/ErrorStore";
import { useGraphInputStore } from "../../store/GraphInputStore";

const { setLeagueError, setModifiersError } = useErrorStore.getState();

/**
 * Checks whether the League input for the graph query is valid
 * @returns boolean
 */
export const checkGraphQueryLeagueInput = () => {
  // If league is empty, return false
  const league = useGraphInputStore.getState().league;
  if (league === "") {
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
  const wantedModifiersExtended = useGraphInputStore
    .getState()
    .wantedModifierExtended.filter(
      (wantedModifierExtended) => wantedModifierExtended.isSelected,
    );

  // If modifiers are empty, return false
  if (wantedModifiersExtended.length === 0) {
    setModifiersError(true);
    return false;
  }
  setModifiersError(false);
  return true;
};
