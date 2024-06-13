from typing import Union
import SimpleITK as sitk
import numpy as np
from .intensity_utils_sitk import rescale_intensity_window_sitk
from .intensity_utils_np import rescale_intensity_window_np



class RescaleImageIntensityPercentile:

    def __init__(self,
                 minimum_percentile: Union[int, float] = None,
                 maximum_percentile: Union[int, float] = None,
                 output_min: Union[int, float] = None,
                 output_max: Union[int, float] = None,
                 *args, **kwargs):

        self.min_percentile = minimum_percentile
        self.max_percentile = maximum_percentile
        self.output_min = output_min
        self.output_max = output_max


    def __call__(self, image: Union[np.array, sitk.Image]) -> Union[np.array, sitk.Image]:


        if isinstance(image, sitk.Image):
            image_np = sitk.GetArrayFromImage(image)
        else:
            image_np = image

        if self.max_percentile is not None:
            pmax = np.percentile(image_np, self.max_percentile)
        else:
            pmax = image_np.max()

        if self.min_percentile is not None:
            pmin = np.percentile(image_np, self.min_percentile)
        else:
            pmin = image_np.min()


        if self.output_min is None:
            self.output_min = pmin

        if self.output_max is None:
            self.output_max = pmax



        if isinstance(image, np.ndarray):
            rescaled_image = rescale_intensity_window_np(image,
                                                       input_min=pmin,
                                                       input_max=pmax,
                                                       output_max=self.output_max,
                                                       output_min=self.output_min)

        elif isinstance(image, sitk.Image):
            rescaled_image = rescale_intensity_window_sitk(image,
                                                           input_min=pmin,
                                                           input_max=pmax,
                                                           output_max=self.output_max,
                                                           output_min=self.output_min)


        else:
            raise ImportError("image must be either a numpy array or a SimpleITK image.")


        return rescaled_image