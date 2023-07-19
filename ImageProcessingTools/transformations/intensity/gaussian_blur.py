from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from ImageProcessingTools.utils import min_max_intensity, clamp_intensity, shift_scale_intensity, rescale_intensity
from ImageProcessingTools.utils import random_uniform_float
from ImageProcessingTools.utils import gaussian_blur



class GaussianBlur:
    def __init__(self,
                 sigma: Union[int, float],
                 *args, **kwargs):

        self.sigma = sigma

    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:


        return gaussian_blur(image,self.sigma, *args, **kwargs)


class RandomGaussianBlur:

    def __init__(self,
                 min_sigma: Union[int, float],
                 max_sigma: Union[int, float],
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, ** kwargs):

        self.min_sigma = min_sigma
        self.max_sigma = max_sigma
        self.seed = seed
        self.legacy_random_state = legacy_random_state


    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:

        sigma = random_uniform_float(low_value=self.min_sigma, high_value=self.max_sigma,
                                     seed=self.seed,
                                     legacy_random_state=self.legacy_random_state)

        return gaussian_blur(image, sigma, *args, **kwargs)



