from typing import Union, Tuple, List
import numpy as np
from ...utils import random_uniform_float
from ...utils.random_float import initialize_rand_state
from .intensity_utils_np import gaussian_blur_np
from .intensity_utils_sitk import gaussian_blur_sitk
import SimpleITK as sitk


class GaussianBlur:
    def __init__(self,
                 sigma: Union[int, float],
                 *args, **kwargs):

        self.sigma = sigma

    def __call__(self,
                 image: Union[np.ndarray, sitk.Image],
                 *args, **kwargs) -> Union[np.ndarray, sitk.Image]:

        if isinstance(image, np.ndarray):
            return gaussian_blur_np(image, self.sigma, *args, **kwargs)

        elif isinstance(image, sitk.Image):
            return gaussian_blur_sitk(image, self.sigma, *args, **kwargs)

        else:
            raise ImportError("Image must be either a numpy array or a SimpleITK image.")

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

        self.rand_init = initialize_rand_state(self.seed, self.legacy_random_state)

    def __call__(self,
                 image: Union[np.ndarray, sitk.Image],
                 *args, **kwargs) -> Union[np.ndarray, sitk.Image]:



        sigma = random_uniform_float(low_value=self.min_sigma, high_value=self.max_sigma,
                                     seed=self.seed,
                                     legacy_random_state=self.legacy_random_state,
                                     rand_init=self.rand_init)


        if isinstance(image, np.ndarray):
            return gaussian_blur_np(image, sigma, *args, **kwargs)

        elif isinstance(image, sitk.Image):
            return gaussian_blur_sitk(image, sigma, *args, **kwargs)

        else:
            raise ImportError("image must be either a numpy array or a SimpleITK image.")



