from __future__ import annotations
from fastapi import APIRouter, Depends
from typing import List, Optional, Union

from app.api.deps import get_db

from app.plotting import plotter_tool

import app.plotting.schemas as schemas

from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/", response_model=schemas.PlotData)
async def get_plot_data(
    query: schemas.PlotQuery, db: Session = Depends(get_db)
):  #: typing TODO
    """
    TODO
    """
    return await plotter_tool.plot(db, query=query)


# Input
# league -> str
# item specifications -> dict
# modifiers w min/max/text rolls -> List

# Output
# value -> List[float]
# dates -> List[datetime]
# most common currency -> str
# most common currency value in chaos -> List[float]
