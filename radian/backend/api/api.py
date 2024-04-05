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
async def make_solid(
    num_samples: Annotated[int, Form()],
    sample_rate: Annotated[int, Form()],
    sides: Annotated[int, Form()],
    r_scale: Annotated[float, Form()],
    core: Annotated[float, Form()],
    z_scale: Annotated[float, Form()],
    build_mode: Annotated[str, Form()],
    file: UploadFile,
    background_tasks: BackgroundTasks
) -> Response:
    
    build_error = ""
    if num_samples < 10 or num_samples > 16000:
        build_error = "Number of Samples Not Within Range"

    if sample_rate < 200 or sample_rate > 16000:
        build_error = "Sample Rate Not Within Range"

    if sides < 3 or sides > 500:
        build_error = "Sides Not Within Range"

    if r_scale < 0.5 or r_scale > 20:
        build_error = "Radial Scale Not Within Range"

    if core < 0.5 or core > 20:
        build_error = "Core Diameter Not Within Range"

    if z_scale < 0.05 or z_scale > 5:
        build_error = "Height Scale Not Within Range"
        
    if build_error != "":
            ret_msg = f"""
                <div  class="container"> 
                    <p>ERROR: {build_error}</p>
                    <button hx-redirect"/" hx-trigger="click">Reload</button>
                </div>
            """
            return HTMLResponse(content=ret_msg)

    print("Building Solid...")
    try:
        now_time = int(time.time())
        stl_file= f"{file.filename[:-4]}{now_time}.stl"
        file_path = f"/tmp/{file.filename[:-4]}{now_time}.wav"
        save_path = f"/tmp/{stl_file}"

        with open(file_path, "wb") as f:
            f.write(file.file.read())
        background_tasks.add_task(delete_file, file_path,180)
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
        background_tasks.add_task(delete_file, save_path,180)
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
                    <p>ERROR: {build_error}</p>
                    <p> Please Reload </p>
                </div>
            """
    except Exception as e:
        print(e)
        ret_msg = f"""
            <div  class="container"> 
                <p>ERROR: {e}</p>
                <p> Please Reload </p>
            </div>
        """

    return HTMLResponse(content=ret_msg)


@router.get("/download/stl/{filename}", response_class=HTMLResponse)
def download_file(filename) -> Response:
    try:
        return FileResponse(f"/tmp/{filename}", media_type='application/octet-stream',filename=f"{filename}")
    except Exception as e:
        print(e)
        