from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from imageprocessingtools.utils import min_max_intensity, clamp_intensity, shift_scale_intensity, rescale_intensity



class RescaleIntensity:
    def __init__(self,
                 new_min: Union[int, float] = None,
                 new_max: Union[int, float] = None,
                 *args, **kwargs):


        self.new_min = new_min
        self.new_max = new_max


    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:


        return rescale_intensity(image,
                                 new_min=self.new_min,
                                 new_max=self.new_max,
                                 *args, **kwargs)
