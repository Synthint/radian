from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
import os
router = APIRouter(prefix="", tags=["webviews"])

@router.get("/", response_class=HTMLResponse)
def main() -> HTMLResponse:
    return HTMLResponse(open("./radian/frontend/index.html").read(), status_code=200)

@router.get("/static/htmxloader", response_class=HTMLResponse)
def htmxloader() -> HTMLResponse:
    return HTMLResponse(open("./radian/static/htmx.min.js").read(), status_code=200)

@router.get("/static/cssloader", response_class=HTMLResponse)
def htmxloader() -> HTMLResponse:
    return HTMLResponse(open("./radian/static/style.css").read(), status_code=200)