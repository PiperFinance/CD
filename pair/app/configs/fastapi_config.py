import os
from fastapi import FastAPI
from typing import Optional
from routers import routers

ALLOWED_HOSTS = ["*"]


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        route.operation_id = route.name  # type:ignore , in this case, 'read_items'


def config(
        DOMAIN: str,
        PORT: int,
        PREFIX: Optional[str] = None):
    '''
    init of Fastapi application :)
    '''
    if PREFIX is not None:
        root_path = PREFIX
    else:
        root_path = "/api/pair"

    app = FastAPI()

    use_route_names_as_operation_ids(
        app)

    app.include_router(routers)

    return app
