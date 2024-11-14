import { PlotQuery, WantedModifier } from "../../client";
import { useErrorStore } from "../../store/ErrorStore";
import { useGraphInputStore } from "../../store/GraphInputStore";
import {
  BaseSpecState,
  WantedModifierExtended,
} from "../../store/StateInterface";

function formatHoursSinceLaunch(hoursSinceLaunch: number): string {
  const daysSinceLaunch = Math.floor(hoursSinceLaunch / 24);
  const remainder = hoursSinceLaunch % 24;

  // Combine the date and time into the desired format
  return `${daysSinceLaunch}T${remainder}`;
}

export default formatHoursSinceLaunch;

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
  if (possibleUniques.length === 0) {
    useErrorStore.getState().setNoRelatedUniqueError(true);
    return;
  } else {
    useErrorStore.getState().setNoRelatedUniqueError(false);
  }
  if (itemName != null) {
    if (!possibleUniques.includes(itemName)) {
      useErrorStore.getState().setItemDoesNotHaveSelectedModifiersError(true);
      return;
    } else {
      useErrorStore.getState().setItemDoesNotHaveSelectedModifiersError(false);
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
  if (baseSpec != null) {
    if (possibleBaseSpecs.length === 1) {
      baseSpec = possibleBaseSpecs[0];
    } else {
      delete baseSpec["baseType"];
    }
  }

  itemSpec = { ...itemSpec, name: possibleUniques.join("|") };
  const wantedModifier: WantedModifier[][] = state.wantedModifierExtended
    .filter((wantedModifier) => wantedModifier.isSelected)
    .reduce((prev, cur, index) => {
      // Very over complicated way to group modifier ids
      const prevLength = prev.length;
      if (prevLength === 0) {
        return [[cur]];
      }
      const wantedModifierIndex = cur.index;
      const prevWantedModifierIndex =
        state.wantedModifierExtended[index - 1].index;

      if (wantedModifierIndex === prevWantedModifierIndex) {
        return [
          ...prev.slice(0, prevLength - 1),
          [...prev[prevLength - 1], cur],
        ];
      }
      return [...prev, [cur]];
    }, [] as WantedModifierExtended[][])
    .map((groupedWantedModifierExtended) =>
      groupedWantedModifierExtended.map((wantedModifierExtended) => ({
        modifierId: wantedModifierExtended.modifierId,
        modifierLimitations: wantedModifierExtended.modifierLimitations,
      })),
    );

  return {
    league: state.league,
    itemSpecifications: itemSpec,
    baseSpecifications: baseSpec,
    wantedModifiers: wantedModifier,
  };
};
