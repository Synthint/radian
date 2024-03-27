import math
import radian.backend.utils.solidlib as solid
import radian.backend.utils.musiclib as music
import numpy as np
from scipy import fft


CORE = 5
SCALE = 10

def wav_to_spiral(samples: np.ndarray, sides: int, height: int = -1, core: int = 1, scale: int = 1, out_of_bounds_mode = "max"):
    if height == -1:
        height = int(samples.size / sides)
    shape = (height,sides)
    cyl = np.zeros(shape)
    sample_index = 0
    for iy, ix in np.ndindex(cyl.shape):
        if out_of_bounds_mode == "max":
            ind = min(sample_index, samples.size)
        elif out_of_bounds_mode == "loop":
            ind = sample_index % samples.size
        cyl[iy,ix] = core + (samples[ind] * scale)
        sample_index += 1
    return cyl


def wav_to_cylinder(samples: np.ndarray, sides: int, height: int = -1, core: int = 1, scale: int = 1, out_of_bounds_mode = "max"):
    if height == -1:
        height = int(samples.size)
    shape = (height,sides)
    cyl = np.zeros(shape)
    sample_index = 0
    for iy in range(height):
        if out_of_bounds_mode == "max":
            ind = min(sample_index, samples.size)
        elif out_of_bounds_mode == "loop":
            ind = sample_index % samples.size
        cyl[iy] = core + (samples[ind] * scale)
        sample_index += 1
    return cyl

def stitch_cylinder(cyl: np.ndarray, z_scale = 1) -> solid:
    tris = []
    height = cyl.shape[0]
    samples = cyl.shape[1]
    # bottom
    for ind in range(samples):
        follow = (ind + 1) % samples
        p1 = solid.point((
                cyl[0,ind] * math.cos(math.pi * 2 * (ind / samples)),
                cyl[0,ind] * math.sin(math.pi * 2 * (ind / samples)),
                0
            ))
        p2 = solid.point((
                cyl[0, follow] * math.cos(math.pi * 2 * (follow / samples)),
                cyl[0, follow] * math.sin(math.pi * 2 * (follow / samples)),
                0
            ))
        p3 = solid.point((0,0,0))
        tris.append(solid.triangle((p1,p2,p3)))
    # sides
    for slice in range(height-1):
        for ind in range(samples):
            follow = (ind + 1) % samples
            p1 = solid.point((
                cyl[slice,ind] * math.cos(math.pi * 2 * (ind / samples)),
                cyl[slice,ind] * math.sin(math.pi * 2 * (ind / samples)),
                slice * z_scale
            ))
            p2 = solid.point((
                cyl[slice, follow] * math.cos(math.pi * 2 * (follow / samples)),
                cyl[slice, follow] * math.sin(math.pi * 2 * (follow / samples)),
                slice * z_scale
            ))
            p3 = solid.point((
                cyl[slice + 1,ind] * math.cos(math.pi * 2 * (ind / samples)),
                cyl[slice + 1,ind] * math.sin(math.pi * 2 * (ind / samples)),
                (slice + 1) * z_scale
            ))
            pA = solid.point((
                cyl[slice + 1, follow] * math.cos(math.pi * 2 * (follow/ samples)),
                cyl[slice + 1, follow] * math.sin(math.pi * 2 * (follow / samples)),
                (slice + 1) * z_scale
            ))
            tris.append(solid.triangle((p1,p2,p3)))
            tris.append(solid.triangle((pA,p2,p3)))
    # top
    for ind in range(samples):
        follow = (ind + 1) % samples
        p1 = solid.point((
                cyl[height-1,ind] * math.cos(math.pi * 2 * (ind / samples)),
                cyl[height-1,ind] * math.sin(math.pi * 2 * (ind / samples)),
                (height-1) * z_scale
            ))
        p2 = solid.point((
                cyl[height-1, follow] * math.cos(math.pi * 2 * (follow / samples)),
                cyl[height-1, follow] * math.sin(math.pi * 2 * (follow / samples)),
                (height-1) * z_scale
            ))
        p3 = solid.point((0, 0, (height-1) * z_scale))

        tris.append(solid.triangle((p1,p2,p3)))

    return solid.solid(triangles=tris)
