import { LeaguesService } from "../../client";
import { QueryClient } from "@tanstack/react-query";

export const useGetLeagues = async (queryClient: QueryClient) => {
  try {
    const leagues = await queryClient.fetchQuery({
      queryKey: ["allModifiers"],
      queryFn: async () => {
        const data = await LeaguesService.getAllLeagues({});
        return Array.isArray(data) ? data : [data];
      },
    });
    return { leagues };
  } catch (error) {
    console.log(error);
    return { leagues: [] };
  }
};
