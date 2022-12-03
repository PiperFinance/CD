import os
from fastapi import FastAPI

from routers import routers

ALLOWED_HOSTS = ["*"]


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        route.operation_id = route.name  # in this case, 'read_items'


def config(
        DOMAIN: str,
        PREFIX: str = None):
    '''
    init of Fastapi application :)
    '''
    if DOMAIN is None:
        DOMAIN = os.getenv("DOMAIN")
        if DOMAIN is None:
            raise ValueError(
                "can't find DOMAIN var in enviromental variables ")
    if PREFIX is not None:
        root_path = PREFIX
    else:
        root_path = "/api/pair"

    print(root_path)
    app = FastAPI()

    use_route_names_as_operation_ids(
        app)


    app.include_router(routers)

    return app
