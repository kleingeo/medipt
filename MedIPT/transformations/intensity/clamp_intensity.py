from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from ...utils import min_max_intensity, clamp_intensity, shift_scale_intensity, rescale_intensity



class ClampIntensity:
    def __init__(self,
                 window_min: Union[int, float] = None,
                 window_max: Union[int, float] = None,
                 *args, **kwargs):

        self.window_min = window_min
        self.window_max = window_max



    def __call__(self, image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:


        return clamp_intensity(image,
                               window_min=self.window_min,
                               window_max=self.window_max,
                               *args, **kwargs)