from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from imageprocessingtools.utils import min_max_intensity, clamp_intensity, shift_scale_intensity, rescale_intensity
from imageprocessingtools.utils import random_uniform_float
from imageprocessingtools.utils import gaussian_blur, gaussian_noise


class GaussianNoise:
    def __init__(self,
                 mean: Union[int, float],
                 sigma: Union[int, float],
                 *args, **kwargs):

        self.sigma = sigma
        self.mean = mean

    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:

        return gaussian_noise(image, self.mean, self.sigma, *args, **kwargs)


class RandomGaussianNoise:

    def __init__(self,
                 sigma: Union[int, float] = None,
                 min_sigma: Union[int, float] = None,
                 max_sigma: Union[int, float] = None,

                 mean: Union[int, float] = None,
                 min_mean: Union[int, float] = None,
                 max_mean: Union[int, float] = None,

                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):

        self.sigma = sigma
        self.min_sigma = min_sigma
        self.max_sigma = max_sigma

        self.mean = mean
        self.min_mean = min_mean
        self.max_mean = max_mean

        self.seed = seed
        self.legacy_random_state = legacy_random_state

    def __call__(self,
                 image: sitk.Image,
                 *args, **kwargs) -> sitk.Image:



        if (self.min_sigma is None) and (self.max_sigma is None) and (self.min_mean is None) and (self.max_mean is None):
            raise ValueError("If all min and max values are none, then use GaussianNoise instead")


        if self.mean is None:
            if (self.min_mean is None) and (self.max_mean is None):
                raise ValueError("If mean is not provided, min_mean and max_mean must be specified")


            mean = random_uniform_float(low_value=self.min_mean, high_value=self.max_mean,
                                        seed=self.seed,
                                        legacy_random_state=self.legacy_random_state)

        else:
            mean = self.mean


        if self.sigma is None:
            if (self.min_sigma is None) and (self.max_sigma is None):
                raise ValueError("If sigma is not provided, min_sigma and max_sigma must be specified")


            sigma = random_uniform_float(low_value=self.min_sigma, high_value=self.max_sigma,
                                        seed=self.seed,
                                        legacy_random_state=self.legacy_random_state)

        else:
            sigma = self.sigma



        return gaussian_noise(image, mean, sigma, *args, **kwargs)



