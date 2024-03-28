import os
import time

from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, Response, JSONResponse, FileResponse
from radian.backend.utils import builder, musiclib
from radian.backend.utils.solidlib import solid


router = APIRouter(prefix="/api", tags=["api"])

def delete_file(file, delay):
    print(f"Delete scheduled for {file} in {delay}s")
    time.sleep(delay)
    print(f"Deleting{file}")
    os.remove(file)




@router.post("/builder/makesolid", response_class=HTMLResponse)
async def make_solid(num_samples: Annotated[int, Form()],
                sample_rate: Annotated[int, Form()],
                sides: Annotated[int, Form()],
                r_scale: Annotated[int, Form()],
                core: Annotated[int, Form()],
                z_scale: Annotated[float, Form()],
                build_mode: Annotated[str, Form()],
                file: UploadFile,
                background_tasks: BackgroundTasks) -> Response:
    
    print("Building Solid...")
    build_error = ""
    try:
        now_time = int(time.time())
        stl_file= f"{file.filename[:-4]}{now_time}.stl"
        file_path = f"/tmp/{file.filename[:-4]}{now_time}.wav"
        save_path = f"/tmp/{stl_file}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())
        print("Opening Wav File")
        wav = musiclib.read(file_path, sample_limit=num_samples, custom_sample_rate=sample_rate)
        if build_mode == "Cylinder":
            wav_solid = builder.wav_to_cylinder(
                samples=wav,
                sides=sides, 
                scale = r_scale,
                core = core,
                )
        elif build_mode == "Spiral":
            wav_solid = builder.wav_to_spiral(
                samples=wav,
                sides=sides, 
                scale = r_scale,
                core = core,
                )
        else:
            build_error = "Improper Build Mode"
        cyl: solid = builder.stitch_cylinder(wav_solid, z_scale = z_scale)
        cyl.save_ascii(f"{stl_file}", save_path)
        print(f"solid saved: {stl_file}")

        if build_error == "":
            ret_msg = f"""
                <div  class="container"> 
                    <a href="/api/download/stl/{stl_file}">Download STL</a>
                    <div hx-get="/viewer/{stl_file}" hx-trigger="load" hx-swap="outerHTML"></div>
                </div>
            """
        else:
            ret_msg = f"""
                <div  class="container"> 
                    ERROR: {build_error}
                </div>
            """
    except Exception as e:
        print(e)
        ret_msg = f"""
            <div  class="container"> 
                ERROR: {e}
            </div>
        """
    background_tasks.add_task(delete_file, file_path,300)
    background_tasks.add_task(delete_file, save_path,300)
    return HTMLResponse(content=ret_msg)


@router.get("/download/stl/{filename}", response_class=HTMLResponse)
def download_file(filename) -> Response:
    try:
        return FileResponse(f"/tmp/{filename}", media_type='application/octet-stream',filename=f"{filename}")
    except Exception as e:
        print(e)
        