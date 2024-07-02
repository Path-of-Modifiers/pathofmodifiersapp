import { QueryClient } from "@tanstack/react-query";
import { GroupedModifierByEffect, ModifiersService } from "../../client";

export const prefetchedGroupedModifiers = async (queryClient: QueryClient) => {
  let groupedModifiers: GroupedModifierByEffect[] = [];

  try {
    // Prefetch all grouped modifiers
    await queryClient.prefetchQuery({
      queryKey: ["prefetchedgroupedmodifiers"],
      queryFn: async () => {
        const data =
          await ModifiersService.getGroupedModifierByEffectApiApiV1ModifierGroupedModifiersByEffectGet();
        if (Array.isArray(data)) {
          groupedModifiers = data;
        } else {
          groupedModifiers = [data];
        }
        return 1;
      },
      staleTime: 10 * 1000, // only prefetch if older than 10 seconds
    });
  } catch (error) {
    console.log(error);
  }

  return { groupedModifiers };
};
