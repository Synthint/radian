import asyncio
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import radian.backend.views.views as webviews
import radian.backend.api.api as apiroutes

def get_app()->FastAPI:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="./radian/static"), name="static")
    app.include_router(webviews.router)
    app.include_router(apiroutes.router)
    return app