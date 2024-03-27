from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
import os
router = APIRouter(prefix="", tags=["webviews"])

@router.get("/", response_class=HTMLResponse)
def main() -> HTMLResponse:
    return HTMLResponse(open("./radian/frontend/index.html").read(), status_code=200)

@router.get("/viewer/{filename}", response_class=HTMLResponse)
def main(filename) -> HTMLResponse:
    return HTMLResponse(open("./radian/frontend/viewer.html").read(), status_code=200)

@router.get("/static/cssloader", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/style.css").read(), status_code=200, media_type="text/css")

@router.get("/static/htmxloader", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/htmx.min.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/wsloader", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/htmx.ws.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/stlloader", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/stlloader.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/three", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/three.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/stlviewer", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/stlviewer.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/orbitcontrols", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/orbitcontrols.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/stats", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/stats.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/gui", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/gui.js").read(), status_code=200, media_type="text/javascript")

@router.get("/static/stlexporter", response_class=Response)
def htmxloader() -> Response:
    return Response(open("./radian/static/stlexporter.js").read(), status_code=200, media_type="text/javascript")
