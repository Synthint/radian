from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sps

def multichannel_to_one(data: np.ndarray) -> np.ndarray:
    new_data = np.zeros(data.shape[0])
    for index in range(data.shape[0]):
        new_data[index] = np.sum(data[index]) / data.shape[1]
    return new_data

def normalize(data: np.ndarray) -> np.ndarray:
    new_data = np.copy(data)
    abs_min = int(abs(np.amin(new_data)))
    abs_max = int(abs(np.amax(new_data)))
    new_data += abs_min
    if abs_min + abs_max == 0:
        abs_min += 1
    np.divide(new_data, abs_min + abs_max, out=new_data, casting="unsafe")
    return new_data

def read(file: str, sample_limit=-1, custom_sample_rate = -1) -> np.ndarray:
    sample_rate, data = wavfile.read(file)
    
    try:
        data2 = multichannel_to_one(data)
    except IndexError:
        print("Song not multichannel, skipping stage")
    
    if custom_sample_rate > 0:
        number_of_samples = round(len(data) * float(custom_sample_rate) / sample_rate)
        data = sps.resample(data, number_of_samples)
    if sample_limit > 0:
        data = data[:sample_limit]
    
    return normalize(data)