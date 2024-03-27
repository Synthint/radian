from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse

from radian.backend.utils import builder, musiclib
from radian.backend.utils.solidlib import solid


router = APIRouter(prefix="/api", tags=["api"])

@router.post("/builder/makesolid", response_class=HTMLResponse)
def make_spiral(file: UploadFile) -> Response:
    try:
        file_path = f"/tmp/{file.filename}"
        save_path = f"/tmp/{file.filename}.stl"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            print("file written")
        wav = musiclib.read(file_path, custom_sample_rate=200)
        print("wav ingested")
        spiral = builder.wav_to_spiral(
            samples=wav,
            sides=20, 
            scale = 3,
            core = 2,
            )
        print("spiral mapped")
        cyl: solid = builder.stitch_cylinder(spiral, z_scale= 0.1)
        print("solid assembled")
        cyl.save_ascii(f"{file.filename}", save_path)
        print("solid saved")

        ret_msg = f"""
            <div  class="container"> 
                <a href="/api/download/stl/{file.filename}">Download STL</a>
                <div hx-get="/viewer/{file.filename}" hx-trigger="load" hx-swap="outerHTML" style="width: 500px; height: 500px" ></div>
            </div>
        """
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
        return FileResponse(f"/tmp/{filename}.stl", media_type='application/octet-stream',filename=f"{filename}.stl")
    except Exception as e:
        print(e)
        ret_msg = f"ERROR: {e}"
        return HTMLResponse(content=ret_msg)