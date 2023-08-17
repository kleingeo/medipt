from typing import Union, Tuple, List
import numpy as np
from .intensity_utils_np import clamp_intensity_np
from .intensity_utils_sitk import clamp_intensity_sitk
import SimpleITK as sitk



class ClampIntensity:
    def __init__(self,
                 window_min: Union[int, float] = None,
                 window_max: Union[int, float] = None,
                 *args, **kwargs):

        self.window_min = window_min
        self.window_max = window_max



    def __call__(self, image: Union[np.ndarray, sitk.Image],
                 *args, **kwargs) -> Union[np.ndarray, sitk.Image]:


        if isinstance(image, np.ndarray):

            return clamp_intensity_np(image,
                                      window_min=self.window_min,
                                      window_max=self.window_max,
                                      *args, **kwargs)

        elif isinstance(image, sitk.Image):
            return clamp_intensity_sitk(image,
                                        window_min=self.window_min,
                                        window_max=self.window_max,
                                        *args, **kwargs)

        else:
            raise ImportError("image must be either a numpy array or a SimpleITK image.")