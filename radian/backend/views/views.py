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
