from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse

from radian.backend.utils import builder, musiclib
from radian.backend.utils import solidlib
from radian.backend.utils.solidlib import solid


router = APIRouter(prefix="/api", tags=["api"])

@router.post("/builder/makespiral", response_class=HTMLResponse)
def make_spiral(file: UploadFile) -> Response:
    try:
        file_path = f"/tmp/{file.filename}"
        save_path = f"/tmp/{file.filename}.stl"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        wav = musiclib.read(file_path, custom_sample_rate=4000)
        spiral = builder.wav_to_spiral(
            samples=wav,
            sides=500, 
            scale = 3,
            core = 2,
            )
        cyl = solidlib.stitch_cylinder(spiral, z_scale= 0.01)
        cyl.save_ascii(f"{file.filename}", save_path)
        return FileResponse(path = save_path)

    except Exception as e:
        print(e)
