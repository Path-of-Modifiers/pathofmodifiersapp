import { useErrorStore } from "../../store/ErrorStore";
import { useGraphInputStore } from "../../store/GraphInputStore";

const { setLeagueError, setModifiersError } = useErrorStore.getState();

/**
 * Checks whether the League input for the graph query is valid
 * @returns boolean
 */
export const checkGraphQueryLeageInput = () => {
    // If league is empty, return false
    const league = useGraphInputStore.getState().plotQuery.league;
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
    const plotModifierQueryStore =
        useGraphInputStore.getState().plotQuery.wantedModifiers;
    // If modifiers are empty, return false
    if (plotModifierQueryStore.length === 0) {
        setModifiersError(true);
        return false;
    }
    setModifiersError(false);
    return true;
};
