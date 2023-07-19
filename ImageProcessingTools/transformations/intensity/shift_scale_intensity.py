from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from ImageProcessingTools.utils import min_max_intensity, clamp_intensity, shift_scale_intensity, rescale_intensity
from ImageProcessingTools.utils import random_uniform_float


class ShiftScaleIntensity:
    def __init__(self,
                 shift: Union[int, float] = None,
                 scale: Union[int, float] = None,
                 *args, **kwargs):

        self.shift = shift
        self.scale = scale


    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:


        output_image = shift_scale_intensity(image,
                                             shift=self.shift,
                                             scale=self.scale,
                                             *args, **kwargs)

        return output_image



class RandomShiftScaleIntensity:

    def __init__(self,
                 shift: Union[int, float] = None,
                 scale: Union[int, float] = None,
                 random_shift: Union[int, float] = None,
                 random_scale: Union[int, float] = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, ** kwargs):

        self.shift = shift
        self.scale = scale

        self.random_shift = random_shift
        self.random_scale = random_scale


        self.seed = seed
        self.legacy_random_state = legacy_random_state


    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:


        output_image = shift_scale_intensity(image,
                                             shift=self.shift,
                                             scale=self.scale,
                                             *args, **kwargs)

        if (self.random_shift is not None) or (self.random_scale is not None):

            random_shift = random_uniform_float(low_value=-self.random_shift,
                                                high_value=self.random_shift,
                                                seed=self.seed,
                                                legacy_random_state=self.legacy_random_state)

            random_scale = random_uniform_float(low_value=-self.random_scale,
                                                high_value=self.random_scale,
                                                seed=self.seed,
                                                legacy_random_state=self.legacy_random_state)

            random_scale = 1 + random_scale

            output_image = shift_scale_intensity(output_image,
                                                 shift=random_shift,
                                                 scale=random_scale,
                                                 *args, **kwargs)

            return output_image

        else:
            return output_image

