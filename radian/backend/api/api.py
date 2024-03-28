from typing import Annotated
from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse

from radian.backend.utils import builder, musiclib
from radian.backend.utils.solidlib import solid


router = APIRouter(prefix="/api", tags=["api"])

@router.post("/builder/makesolid", response_class=HTMLResponse)
def make_spiral(num_samples: Annotated[str, Form()],
                sample_rate: Annotated[str, Form()],
                sides: Annotated[str, Form()],
                r_scale: Annotated[str, Form()],
                core: Annotated[str, Form()],
                z_scale: Annotated[str, Form()],
                build_mode: Annotated[str, Form()],
                file: UploadFile) -> Response:
    
    try:
        stl_file= f"{file.filename[:-4]}.stl"
        file_path = f"/tmp/{file.filename}"
        save_path = f"/tmp/{stl_file}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        wav = musiclib.read(file_path, custom_sample_rate=20)
        spiral = builder.wav_to_spiral(
            samples=wav,
            sides=5, 
            scale = 2,
            core = 5,
            )
        cyl: solid = builder.stitch_cylinder(spiral, z_scale= 1.5)
        cyl.save_ascii(f"{stl_file}", save_path)
        print(f"solid saved: {stl_file}")
        ret_msg = f"""
            <div  class="container"> 
                <a href="/api/download/stl/{stl_file}">Download STL</a>
                <div hx-get="/viewer/{stl_file}" hx-trigger="load" hx-swap="outerHTML"></div>
            </div>
        """
        print()
    except Exception as e:
        print(e)
        ret_msg = f"""
            <div  class="container"> 
                ERROR: {e}
            </div>
        """
    return HTMLResponse(content=ret_msg)


@router.get("/download/stl/{filename}", response_class=HTMLResponse)
def make_spiral(filename) -> Response:
    try:
        return FileResponse(f"/tmp/{filename}", media_type='application/octet-stream',filename=f"{filename}")
    except Exception as e:
        print(e)
        