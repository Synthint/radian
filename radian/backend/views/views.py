from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="./radian/frontend/templates")

router = APIRouter(prefix="", tags=["webviews"])




@router.get("/", response_class=HTMLResponse)
def main() -> HTMLResponse:
    return HTMLResponse(open("./radian/frontend/index.html").read(), status_code=200)

@router.get("/viewer/{filename}", response_class=HTMLResponse)
def main(request: Request, filename: str) -> HTMLResponse:
    return templates.TemplateResponse( request=request, name="viewer.html", context={"filename": f"/api/download/stl/{filename}"})
