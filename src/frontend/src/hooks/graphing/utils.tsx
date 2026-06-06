import { PlotQuery } from "../../client";
import { useErrorStore } from "../../store/ErrorStore";
import { useGraphInputStore } from "../../store/GraphInputStore";
import {
  BaseSpecState,
  GraphInputState,
  ModifierLimitationState,
} from "../../store/StateInterface";
import { LEAGUE_LAUNCH_TIME, PLOTTING_WINDOW_HOURS } from "../../config";

export const LEAGUE_LAUNCH_DATETIME = new Date(LEAGUE_LAUNCH_TIME);

const calcMean = (values: number[]) => {
  const sumValues = values.reduce((prev, cur) => prev + cur, 0);
  return sumValues / values.length;
};

const calcSTD = (values: number[], mean: number) => {
  return Math.sqrt(
    values.reduce((prev, cur) => prev + (cur - mean) * (cur - mean), 0) /
      values.length,
  );
};

export const findWinsorUpperBound = (values: number[]) => {
  const mean = calcMean(values);
  const std = calcSTD(values, mean);

  const upperBoundry = Math.ceil(mean + 1.96 * std);
  return upperBoundry;
};

export function formatHoursSinceLaunch(hoursSinceLaunch: number): string {
  const daysSinceLaunch = Math.floor(hoursSinceLaunch / 24);
  const remainder = hoursSinceLaunch % 24;

  // Combine the date and time into the desired format
  return `${daysSinceLaunch}T${remainder}`;
}

export const getHoursSinceLaunch = (currentTime: Date): number => {
  const getCurrentTimeDate = currentTime.getTime();
  const hoursSinceLaunch = Math.floor(
    (getCurrentTimeDate - LEAGUE_LAUNCH_DATETIME.getTime()) / (1000 * 3600),
  );
  return hoursSinceLaunch;
};

const removeNumericalRoll = (
  modifierLimitations: ModifierLimitationState[] | null | undefined,
  position: number,
  rollType: "min" | "max",
) => {
  if (modifierLimitations == null) {
    return false;
  }
  for (let i = 0; i < modifierLimitations.length; i++) {
    const limitation = modifierLimitations[i];
    if (limitation.position === position) {
      const minRoll = limitation.minRoll;
      const maxRoll = limitation.maxRoll;
      // checks if all rolls will be gone after deletion
      if (
        (!minRoll || rollType === "min") &&
        (!maxRoll || rollType === "max")
      ) {
        delete modifierLimitations[i];
        if (modifierLimitations.length === 1) {
          return true;
        }
      } else {
        delete limitation[rollType === "min" ? "minRoll" : "maxRoll"];
      }
      return false;
    }
  }
};

const addNumericalRoll = (
  modifierLimitations: ModifierLimitationState[] | null | undefined,
  position: number,
  roll: number,
  rollType: "min" | "max",
) => {
  let modifierLimitation: ModifierLimitationState;
  if (!modifierLimitations) {
    modifierLimitations = [];
    modifierLimitation = {
      position: position,
    };
    modifierLimitations.push(modifierLimitation);
  } else {
    const idx = modifierLimitations.findIndex(
      (modifierLimitation) => modifierLimitation.position === position,
    );
    if (idx === -1) {
      modifierLimitation = {
        position: position,
      };
      modifierLimitations.push(modifierLimitation);
    } else {
      modifierLimitation = modifierLimitations[idx];
    }
  }
  modifierLimitation[rollType === "min" ? "minRoll" : "maxRoll"] = roll;
  return modifierLimitations;
};

export const updateNumericalRoll = (
  state: GraphInputState,
  modifierId: number,
  position: number,
  roll: number | undefined,
  rollType: "min" | "max",
  index: number,
) => {
  const updatedModifiersExtended = state.wantedModifierExtended.map(
    (wantedModifierExtended) => {
      if (
        wantedModifierExtended.modifierId === modifierId &&
        wantedModifierExtended.index === index
      ) {
        // roll is undefined => delete roll
        if (roll === undefined) {
          const noMoreLimitations = removeNumericalRoll(
            wantedModifierExtended.modifierLimitations,
            position,
            rollType,
          );
          if (noMoreLimitations) {
            return {
              ...wantedModifierExtended,
              modifierLimitations: null,
            };
          }
        } else {
          const updatedModifierLimitations = addNumericalRoll(
            wantedModifierExtended.modifierLimitations,
            position,
            roll,
            rollType,
          );
          return {
            ...wantedModifierExtended,
            modifierLimitations: updatedModifierLimitations,
          };
        }
      }
      return wantedModifierExtended;
    },
  );
  return { wantedModifierExtended: updatedModifiersExtended };
};

export const getOptimizedPlotQuery = (): PlotQuery | undefined => {
  // currently always runs, needs to be in if check
  // when Non-unique rarity is possible
  const state = useGraphInputStore.getState();
  const itemName = state.itemName;
  let itemSpec = state.itemSpec;
  let baseSpec = state.baseSpec;
  let possibleUniques = state.wantedModifierExtended.reduce(
    (prev, cur, index) => {
      if (cur.relatedUniques === undefined || !cur.isSelected) {
        return prev;
      }

      const newUniqueCandidates = cur.relatedUniques.split("|");
      if (index === 0) {
        return newUniqueCandidates;
      }
      return prev.filter((prevCandidate) =>
        newUniqueCandidates.includes(prevCandidate),
      );
    },
    [] as string[],
  );
  if (possibleUniques.length === 0 && state.itemSpec?.identified !== false) {
    useErrorStore.getState().setNoRelatedUniqueError(true);
    return;
  } else {
    useErrorStore.getState().setNoRelatedUniqueError(false);
  }
  if (itemName != null) {
    if (!possibleUniques.includes(itemName) && itemSpec?.identified !== false) {
      useErrorStore.getState().setCurrentlySelectedModifiersError(true);
      return;
    } else {
      useErrorStore.getState().setCurrentlySelectedModifiersError(false);
    }
    possibleUniques = [itemName];
  }
  // Only applicable if rarity is unique and base spec is not already
  // chosen
  const possibleBaseSpecs = state.choosableItemBaseType.reduce((prev, cur) => {
    if (cur.relatedUniques == null) {
      return prev;
    }
    const relatedUniques = cur.relatedUniques.split("|");
    if (possibleUniques.some((unique) => relatedUniques.includes(unique))) {
      if (
        !baseSpec ||
        ((!baseSpec.itemBaseTypeId ||
          baseSpec.itemBaseTypeId === cur.itemBaseTypeId) &&
          (!baseSpec.category || baseSpec.category === cur.category) &&
          (!baseSpec.subCategory || baseSpec.subCategory === cur.subCategory))
      ) {
        return [
          ...prev,
          {
            itemBaseTypeId: cur.itemBaseTypeId,
            category: baseSpec?.category,
            subCategory: baseSpec?.subCategory,
          },
        ];
      }
    }
    return prev;
  }, [] as BaseSpecState[]);

  if (possibleBaseSpecs.length === 0) {
    useErrorStore.getState().setBaseSpecDoesNotMatchError(true);
    return;
  } else {
    useErrorStore.getState().setBaseSpecDoesNotMatchError(false);
  }
  if (possibleBaseSpecs.length === 1) {
    baseSpec = possibleBaseSpecs[0];
  }
  if (baseSpec?.baseType != null) {
    delete baseSpec["baseType"];
  }

  itemSpec = { ...itemSpec, name: possibleUniques.join("|") };
  const wantedModifier = state.wantedModifierExtended
    .filter((wantedModifier) => wantedModifier.isSelected)
    .map((wantedMoidifierExtended) => ({
      modifierId: wantedMoidifierExtended.modifierId,
      modifierLimitations: wantedMoidifierExtended.modifierLimitations,
    }));
  const currentTime = new Date();
  const end = getHoursSinceLaunch(currentTime);
  const window = PLOTTING_WINDOW_HOURS;
  const start = end - window;

  return {
    league: state.leagues,
    itemSpecifications: itemSpec,
    baseSpecifications: baseSpec,
    wantedModifiers: wantedModifier,
    start: start,
    end: end,
  };
};
