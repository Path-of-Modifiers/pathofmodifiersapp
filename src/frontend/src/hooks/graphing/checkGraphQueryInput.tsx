import { useErrorStore } from "../../store/ErrorStore";
import { useGraphInputStore } from "../../store/GraphInputStore";

const { setLeagueError, setNoSelectedModifiersError, setModifiersUnidentifiedError } = useErrorStore.getState();

/**
 * Checks whether the League input for the graph query is valid
 * @returns boolean
 */
export const checkGraphQueryLeagueInput = () => {
  // If league is empty, return false
  const leagues = useGraphInputStore.getState().leagues;
  if (leagues.length === 0) {
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
  const falseItemSpecIdentified = useGraphInputStore.getState().itemSpec?.identified === false

  // If modifiers are empty, return false
  if (wantedModifiersExtended.length === 0 && !falseItemSpecIdentified) {
    setNoSelectedModifiersError(true);
    return false;
  } else {
    setNoSelectedModifiersError(false);
  }

  if (wantedModifiersExtended.length !== 0 && falseItemSpecIdentified) {
    setModifiersUnidentifiedError(true);
    return false
  } else {
    setModifiersUnidentifiedError(false);
  }

  return true;
};
