from typing import Any

from sqlalchemy.orm import Session

from app.core.models.models import (
    League as model_League,
)
from app.core.models.models import (
    Modifier as model_Modifier,
)
from app.tests.utils.model_utils.item_modifier import (
    generate_random_item_modifier,
)


async def create_minimal_random_plot_query_dict(db: Session) -> dict[str, Any]:
    """
    Create a random plot query dictionary.

    Returns:
        Dict: plot query dictionary with random values.
    """
    _, _, item_modifier_deps = await generate_random_item_modifier(
        db, retrieve_dependencies=True
    )

    league_dep: model_League = item_modifier_deps[-3]
    modifier_dep: model_Modifier = item_modifier_deps[-1]

    wanted_modifiers = [
        {
            "modifierId": modifier_dep.modifierId,
        }
    ]

    plot_query = {
        "leagueId": league_dep.leagueId,
        "wantedModifiers": wanted_modifiers,
    }

    return plot_query
