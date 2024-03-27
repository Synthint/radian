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


