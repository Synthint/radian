from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse

from radian.backend.utils import builder, musiclib
from radian.backend.utils.solidlib import solid


router = APIRouter(prefix="/api", tags=["api"])

@router.post("/builder/makesolid", response_class=HTMLResponse)
def make_spiral(file: UploadFile) -> Response:

    try:
        stl_file= f"{file.filename[:-4]}.stl"
        file_path = f"/tmp/{file.filename}"
        save_path = f"/tmp/{stl_file}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
            print("file written")
        wav = musiclib.read(file_path, custom_sample_rate=600)
        print("wav ingested")
        spiral = builder.wav_to_spiral(
            samples=wav,
            sides=6, 
            scale = 2,
            core = 20,
            )
        print("spiral mapped")
        cyl: solid = builder.stitch_cylinder(spiral, z_scale= 1)
        print("solid assembled")
        cyl.save_ascii(f"{stl_file}", save_path)
        print(f"solid saved: {stl_file}")
        ret_msg = f"""
            <div  class="container"> 
                <a href="/api/download/stl/{stl_file}">Download STL</a>
                <div hx-get="/viewer/{stl_file}" hx-trigger="load" hx-swap="outerHTML" style="width: 500px; height: 500px" ></div>
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
        return FileResponse(f"/opt/radian/static/{filename}", media_type='application/octet-stream',filename=f"{filename}")
    except Exception as e:
        print(e)
        