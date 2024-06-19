from typing import Union, Tuple, List
import numpy as np
from .intensity_utils_sitk import shift_scale_intensity_sitk
from .intensity_utils_np import shift_scale_intensity_np
from ...utils import random_uniform_float
from ...utils.random_float import initialize_rand_state
import SimpleITK as sitk
import warnings


# class ShiftScaleIntensity:
#     def __init__(self,
#                  shift: Union[int, float] = None,
#                  scale: Union[int, float] = None,
#                  *args, **kwargs):
#
#         self.shift = shift
#         self.scale = scale
#
#
#     def __call__(self,
#                  image: Union[np.ndarray, sitk.Image],
#                  *args, **kwargs) -> Union[np.ndarray, sitk.Image]:
#
#         if isinstance(image, np.ndarray):
#             output_image = shift_scale_intensity_np(image,
#                                                     shift=self.shift,
#                                                     scale=self.scale,
#                                                     *args, **kwargs)
#         elif isinstance(image, sitk.Image):
#             output_image = shift_scale_intensity_sitk(image,
#                                                       shift=self.shift,
#                                                       scale=self.scale,
#                                                       *args, **kwargs)
#
#         else:
#             raise ImportError("image must be either a numpy array or a SimpleITK image.")
#
#         return output_image



class ShiftScaleIntensity:

    def __init__(self,
                 shift: Union[int, float] = None,
                 scale: Union[int, float] = None,
                 input_min: Union[int, float] = None,
                 input_max: Union[int, float] = None,
                 output_min: Union[int, float] = None,
                 output_max: Union[int, float] = None,
                 random_shift: Union[int, float] = None,
                 random_scale: Union[int, float] = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, ** kwargs):

        self.shift = shift
        self.scale = scale


        self.input_min = input_min
        self.input_max = input_max
        self.output_min = output_min
        self.output_max = output_max

        self.random_shift = random_shift
        self.random_scale = random_scale


        self.seed = seed
        self.legacy_random_state = legacy_random_state

        self.rand_init = initialize_rand_state(self.seed, self.legacy_random_state)


    def __call__(self,
                 image: Union[np.ndarray, sitk.Image],
                 *args, **kwargs) -> Union[np.ndarray, sitk.Image]:


        if (self.shift is None) and (self.scale is None) and (self.input_min is None) and (self.input_max is None) and (self.output_min is None) and (self.output_max is None):
            raise ValueError("At least one of shift, scale, input_min, input_max, output_min, output_max must be provided.")


        if ((self.shift is None) and (self.scale is None)) and ((self.input_min is None) and (self.input_max is None) and (self.output_min is None) and (self.output_max is None)):
            raise ValueError("Either shift and scale or input_min, input_max, output_min, output_max must be provided.")

        if (self.shift is not None) and (self.scale is not None) and (self.input_min is not None) and (self.input_max is not None) and (self.output_min is not None) and (self.output_max is not None):
            warnings.warn("Mixing both shift and scale with input_min, input_max, output_min, output_max. Input and output values will be set to 'None'.")
            self.input_min = None
            self.input_max = None
            self.output_min = None
            self.output_max = None


        if (self.shift is None) and (self.scale is None) and (self.input_min is not None) and (self.input_max is not None) and (self.output_min is not None) and (self.output_max is not None):
            self.shift = -self.input_min + self.output_min * (self.input_max - self.input_min) / (self.output_max - self.output_min)
            self.scale = (self.output_max - self.output_min) / (self.input_max - self.input_min)




        if isinstance(image, np.ndarray):
            output_image = shift_scale_intensity_np(image,
                                                    shift=self.shift,
                                                    scale=self.scale,
                                                    *args, **kwargs)

        elif isinstance(image, sitk.Image):
            output_image = shift_scale_intensity_sitk(image,
                                                      shift=self.shift,
                                                      scale=self.scale,
                                                      *args, **kwargs)

        else:
            raise ImportError("image must be either a numpy array or a SimpleITK image.")


        if (self.random_shift is not None) or (self.random_scale is not None):

            if self.random_shift:
                random_shift = random_uniform_float(low_value=-self.random_shift,
                                                    high_value=self.random_shift,
                                                    seed=self.seed,
                                                    legacy_random_state=self.legacy_random_state,
                                                    rand_init=self.rand_init)

            else:
                random_shift = 0

            if self.random_scale:
                random_scale = random_uniform_float(low_value=-self.random_scale,
                                                    high_value=self.random_scale,
                                                    seed=self.seed,
                                                    legacy_random_state=self.legacy_random_state,
                                                    rand_init=self.rand_init)

            else:
                random_scale = 1

            random_scale = 1 + random_scale

            if isinstance(image, np.ndarray):
                output_image = shift_scale_intensity_np(output_image,
                                                        shift=random_shift,
                                                        scale=random_scale,
                                                        *args, **kwargs)

            elif isinstance(image, sitk.Image):
                output_image = shift_scale_intensity_sitk(output_image,
                                                          shift=random_shift,
                                                          scale=random_scale,
                                                          *args, **kwargs)

            return output_image

        else:

            return output_image

