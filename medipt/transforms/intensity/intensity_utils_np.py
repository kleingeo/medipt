import SimpleITK as sitk
import numpy as np
from scipy.ndimage import gaussian_filter
from typing import Union, Tuple, List, Any, Callable, Optional
from types import ModuleType


def clamp_intensity_np(image: np.ndarray,
                       window_min: Union[int, float] = None,
                       window_max: Union[int, float] = None,
                       image_min: Union[int, float] = None,
                       image_max: Union[int, float] = None,
                       *args, **kwargs) -> np.ndarray:


    if (window_min is None) and (window_max is None):
        raise ValueError('window_min and window_max cannot both be None.')

    if image_min is None or image_max is None:
        if image_min is None:
            image_min = image.min()
        if image_max is None:
            image_max = image.max()

    if window_min is None:
        window_min = image_min
    if window_max is None:
        window_max = image_max

    clamped_image = np.clip(image, window_min, window_max)

    return clamped_image



def shift_scale_intensity_np(image: np.ndarray,
                             shift: Union[int, float] = None,
                             scale: Union[int, float] = None,
                             *args, **kwargs) -> np.ndarray:

    shifted_image = image + shift
    rescaled_image = shifted_image * scale

    return rescaled_image


def rescale_intensity_np(image: np.ndarray,
                         new_min: Union[int, float] = None,
                         new_max: Union[int, float] = None,
                         *args, **kwargs) -> np.ndarray:

    if (new_min is None) or (new_max is None):
        if new_min is None:
            new_min = image.min()
        if new_max is None:
            new_max = image.min()

    rescaled_image = (image - new_min) / (new_max - new_min)
    return rescaled_image




def gaussian_blur_np(image: np.ndarray,
                     sigma: Union[int, float],
                     *args, **kwargs) -> np.ndarray:
    output_image = gaussian_filter(image, sigma=sigma)

    return output_image



def gaussian_noise_np(image: np.ndarray,
                      mean: Union[int, float],
                      sigma: Union[int, float],
                      rand_init: Union[ModuleType, np.random.Generator, np.random.BitGenerator] = None,
                      *args, **kwargs) -> np.ndarray:

    gaussian = rand_init.normal(mean, sigma, image.shape)
    output_image = image + gaussian
    return output_image