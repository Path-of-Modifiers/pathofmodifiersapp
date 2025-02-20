import { useQueryClient } from "@tanstack/react-query";
import { ModifiersService } from "../../client";

export const useGetGroupedModifiers = async () => {
    const queryClient = useQueryClient();

    try {
        // Fetch and return the grouped modifiers directly
        const groupedModifiers = await queryClient.fetchQuery({
            queryKey: ["prefetchedGroupedModifiers"],
            queryFn: async () => {
                const fetchedData =
                    await ModifiersService.getGroupedModifierByEffect();
                return Array.isArray(fetchedData) ? fetchedData : [fetchedData];
            },
        });

        return { groupedModifiers };
    } catch (error) {
        console.log(error);
        return { groupedModifiers: [] }; // Return an empty array on error
    }
};
