from backend_api.app.core.schemas.league import League, LeagueCreate, LeagueUpdate

from data_retrieval_app.data_deposit.data_depositor_base import DataDepositorBase
from data_retrieval_app.utils import get_leagues


class LeagueDataDepositor(DataDepositorBase[League, LeagueCreate, LeagueUpdate]):
    def __init__(self) -> None:
        super().__init__(data_type="league", update_model=LeagueUpdate)

        self.update_url = str(self.data_url)
        self.data_url += "?on_duplicate_pkey_do_nothing=true"
        self.current_data_by_unique_key = self._get_current_leagues()

    def _get_current_leagues(self) -> dict[str, League]:
        leagues = get_leagues(self.pom_auth_headers)

        return {league.name: league for league in leagues}

    def _check_for_complex_updates(self, new_data, current, updated):
        return False, updated

    def _preprocess_data(self, data):
        deposit_leagues = list[LeagueCreate]()
        for league in data:
            for key in list(league.keys()):
                if league[key] == "":
                    league.pop(key)

            deposit_leagues.extend(
                [
                    LeagueCreate(
                        name=league["name"],
                        validFrom=league["validFrom"],
                        validTo=league.get("validTo"),
                        version=league["version"],
                    ),
                    LeagueCreate(
                        name=f"Hardcore {league["name"]}",
                        validFrom=league["validFrom"],
                        validTo=league.get("validTo"),
                        version=league["version"],
                    ),
                ]
            )

        return deposit_leagues

    def _process_data(self, data):
        data = self._remove_duplicates(data, primary_key="leagueId", unique_key="name")
        return data
