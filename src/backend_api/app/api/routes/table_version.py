from typing import Annotated

from backend_api.app.api.deps import (
    get_current_active_superuser,
    get_db,
)
from backend_api.app.api.params import FilterParams
from backend_api.app.core.rate_limit.rate_limit_config import rate_limit_settings
from backend_api.app.core.rate_limit.rate_limiters import (
    apply_user_rate_limits,
)
from backend_api.app.crud import CRUD_tableVersion
from backend_api.app.exceptions.model_exceptions.db_exception import (
    DbObjectDoesNotExistError,
)
from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.orm import Session

import app.core.schemas as schemas

router = APIRouter()


table_version_prefix = "tableVersion"


@router.get(
    "/{tableName}",
    response_model=schemas.TableVersion | list[schemas.TableVersion] | None,
    dependencies=[Depends(get_current_active_superuser)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_table_version(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    tableName: str,
    db: Session = Depends(get_db),
):
    """
    Get table_version or list of table_versions by key and
    value for "tableName"

    Dominant key is "tableName".

    Returns one or a list of table_versions.
    """

    table_version_map = {"tableName": tableName}
    try:
        table_version = await CRUD_tableVersion.get(db=db, filter=table_version_map)
    except DbObjectDoesNotExistError:
        return None

    return table_version


@router.get(
    "/",
    response_model=schemas.TableVersion | list[schemas.TableVersion],
    dependencies=[Depends(get_current_active_superuser)],
)
@apply_user_rate_limits(
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_SECOND,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_MINUTE,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_HOUR,
    rate_limit_settings.DEFAULT_USER_RATE_LIMIT_DAY,
)
async def get_all_table_versions(
    request: Request,  # noqa: ARG001
    response: Response,  # noqa: ARG001
    filter_params: Annotated[FilterParams, Query()],
    db: Session = Depends(get_db),
):
    """
    Get all table versions.

    Returns a list of all table_versions.
    """

    all_table_versions = await CRUD_tableVersion.get(db=db, filter_params=filter_params)

    return all_table_versions


@router.post(
    "/",
    response_model=schemas.TableVersion | list[schemas.TableVersion],
    dependencies=[Depends(get_current_active_superuser)],
)
async def create_table_version(
    table_versions: schemas.TableVersionCreate | list[schemas.TableVersionCreate],
    return_nothing: bool | None = None,
    db: Session = Depends(get_db),
):
    """
    Create a list of new table versions.
    """

    return await CRUD_tableVersion.create(
        db=db, obj_in=table_versions, return_nothing=return_nothing
    )


@router.put(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
)
async def update_table_version(
    table_version_update: schemas.TableVersionUpdate,
    db: Session = Depends(get_db),
):
    """
    Returns the updated table version.
    """

    table_version_item_map = {"tableName": table_version_update.tableName}

    table_version_item = await CRUD_tableVersion.get(
        db=db,
        filter=table_version_item_map,
    )

    return await CRUD_tableVersion.update(
        db_obj=table_version_item, obj_in=table_version_update, db=db
    )
