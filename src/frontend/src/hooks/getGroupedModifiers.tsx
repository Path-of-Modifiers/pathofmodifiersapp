import { useState } from "react";
import { ModifiersService, GroupedModifierByEffect } from "../client";
import { useQuery } from "@tanstack/react-query";

// Get all grouped modifiers by effect
export const GetGroupedModifiersByEffect = () => {
  const [modifiers, setModifiers] = useState<
    GroupedModifierByEffect | GroupedModifierByEffect[]
  >([]);
  try {
    useQuery({
      queryKey: ["allModifiers"],
      queryFn: async () => {
        setModifiers(
          await ModifiersService.getGroupedModifierByEffectApiApiV1ModifierGroupedModifiersByEffectGet()
        );
        return 1;
      },
    });
    if (Array.isArray(modifiers)) {
      return modifiers; // If modifiers is already an array, return it directly
    } else {
      return [modifiers]; // If modifiers is not an array, wrap it in an array
    }
  } catch (error) {
    console.log(error);
  }
};
