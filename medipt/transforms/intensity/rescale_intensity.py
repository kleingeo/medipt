from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from .intensity_utils_np import rescale_intensity_np
from .intensity_utils_sitk import rescale_intensity_sitk



class RescaleIntensity:
    def __init__(self,
                 new_min: Union[int, float] = None,
                 new_max: Union[int, float] = None,
                 *args, **kwargs):


        self.new_min = new_min
        self.new_max = new_max


    def __call__(self,
                 image: Union[np.ndarray, sitk.Image],
                 *args, **kwargs) -> Union[np.ndarray, sitk.Image]:


        if isinstance(image, np.ndarray):
            return rescale_intensity_np(image,
                                        output_min=self.new_min,
                                        output_max=self.new_max,
                                        *args, **kwargs)

        elif isinstance(image, sitk.Image):
            return rescale_intensity_sitk(image,
                                          output_min=self.new_min,
                                          output_max=self.new_max,
                                          *args, **kwargs)

        else:
            raise ImportError("image must be either a numpy array or a SimpleITK image.")