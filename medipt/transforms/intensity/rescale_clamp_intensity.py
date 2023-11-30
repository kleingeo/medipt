from typing import Union, Tuple, List
import numpy as np
from .intensity_utils_np import clamp_intensity_np
from .intensity_utils_sitk import clamp_intensity_sitk


def rescale_clamp_intensity(image: np.ndarray,
                            new_min: Union[int, float] = None,
                            new_max: Union[int, float] = None,
                            window_min: Union[int, float] = None,
                            window_max: Union[int, float] = None,
                            shift: Union[int, float] = None,
                            scale: Union[int, float] = None,
                            random_shift: Union[int, float] = None,
                            random_scale: Union[int, float] = None,
                            *args, **kwargs):


    output_image = image

    image_min = image.min()
    image_max = image.max()


    if (window_min is not None) or (window_max is not None):

        output_image = clamp_intensity_np(output_image,
                                            window_min=window_min,
                                            window_max=window_max,
                                            image_min=image_min,
                                            image_max=image_max,
                                            *args, **kwargs)




    if (new_min is not None) or (new_max is not None):

        if new_min is None:
            new_min = window_min if window_min is not None else image_min

        if new_max is None:
            new_max = window_max if window_max is not None else image_max


        current_min = window_min if window_min is not None else image_min
        current_max = window_max if window_max is not None else image_max

        intens_scaling = (new_max - new_min) / (current_max - current_min)
        shift = new_min - intens_scaling * current_min



        a = 1



    if (shift is None) or (scale is None):


        current_min = image.min()
        current_max = image.max()


        scale = (new_max - new_min) / (current_max - current_min)

        shift = new_min - scale * current_min


class RescaleClampIntensity:
    def __init__(self,
                 new_min: Union[int, float] = None,
                 new_max: Union[int, float] = None,
                 window_min: Union[int, float] = None,
                 window_max: Union[int, float] = None,
                 shift: Union[int, float] = None,
                 scale: Union[int, float] = None,
                 *args, **kwargs):

        self.new_min = new_min
        self.new_max = new_max

        self.window_min = window_min
        self.window_max = window_max

        self.shift = shift
        self.scale = scale



        # pre-processing: clamp image intensity so minimum is -1024

        # apply transforms

        # post_processing:
            # shift image by minimum and scale by 1/2048
                # this tries to put image between -1 and 1

            # apply random shifts and scales, this is why we put image between -1 and 1

            # clamp image intensity between -1 and 1


    def rescale_intensity(self,
                          image: np.ndarray,
                          *args, **kwargs):


        scaled_image = rescale_clamp_intensity(image,
                                               new_min=self.new_min,
                                               new_max=self.new_max,
                                               window_min=self.window_min,
                                               window_max=self.window_max,
                                               shift=self.shift,
                                               scale=self.scale,
                                               *args, **kwargs)

        return scaled_image

