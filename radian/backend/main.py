from fastapi import FastAPI
import radian.backend.views.views as webviews
import radian.backend.api.api as apiroutes


def get_app()->FastAPI:
    app = FastAPI()
    app.include_router(webviews.router)
    app.include_router(apiroutes.router)
    return app