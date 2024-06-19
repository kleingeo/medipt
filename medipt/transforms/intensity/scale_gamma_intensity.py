from typing import Union, Tuple, List
import numpy as np
from .intensity_utils_sitk import shift_scale_intensity_sitk
from .intensity_utils_np import shift_scale_intensity_np
from ...utils import random_uniform_float
from ...utils.random_float import initialize_rand_state
import SimpleITK as sitk
import warnings
from .shift_scale_intensity import ShiftScaleIntensity
from .intensity_utils_sitk import min_max_intensity_sitk, change_image_gamma_sitk
from .intensity_utils_np import change_image_gamma_np








class ScaleGammaIntensity:
    def __init__(self,
                 gamma: Union[int, float] = None,
                 min_random_gamma: Union[int, float] = None,
                 max_random_gamma: Union[int, float] = None,
                 output_min: Union[int, float] = None,
                 output_max: Union[int, float] = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):

        self.gamma = gamma

        self.min_random_gamma = min_random_gamma
        self.max_random_gamma = max_random_gamma

        self.output_min = output_min
        self.output_max = output_max

        self.seed = seed
        self.legacy_random_state = legacy_random_state

        self.rand_init = initialize_rand_state(self.seed, self.legacy_random_state)


    def __call__(self,
                 image: Union[np.ndarray, sitk.Image],
                 *args, **kwargs) -> Union[np.ndarray, sitk.Image]:


        if (self.gamma is None) and (self.min_random_gamma is None) and (self.max_random_gamma is None):
            raise ValueError("gamma or min_random_gamma and max_random_gamma must be specified.")


        if (self.gamma is None) and ((self.min_random_gamma is None) or (self.max_random_gamma is None)):
            raise ValueError("min_random_gamma and max_random_gamma must be specified together.")

        if (self.gamma is not None) and (self.min_random_gamma is not None) and (self.max_random_gamma is not None):
            warnings.warn("Mixing both random and non-random gamma. Random gammas will be set to 'None'.")

            self.min_random_gamma = None
            self.max_random_gamma = None

        if (self.gamma is None) and (self.min_random_gamma is not None) and (self.max_random_gamma is not None):
            random_gamma = random_uniform_float(self.min_random_gamma, self.max_random_gamma,
                                                seed=self.seed, legacy_random_state=self.legacy_random_state,
                                                rand_init=self.rand_init
                                                )

            self.gamma = random_gamma


        if isinstance(image, np.ndarray):
            input_min = image.min()
            input_max = image.max()

        elif isinstance(image, sitk.Image):
            input_min, input_max = min_max_intensity_sitk(image)

        else:
            raise ImportError("Image must be either a numpy array or a SimpleITK image.")

        shift_scale_image = ShiftScaleIntensity(input_min=input_min, input_max=input_max, output_min=self.output_min, output_max=self.output_max,
                                                seed=self.seed,
                                                legacy_random_state=self.legacy_random_state, *args, **kwargs)

        image = shift_scale_image(image, *args, **kwargs)



        if isinstance(image, np.ndarray):
            image = change_image_gamma_np(image, gamma=self.gamma, *args, **kwargs)

        elif isinstance(image, sitk.Image):
            image = change_image_gamma_sitk(image, gamma=self.gamma, *args, **kwargs)



        shift_scale_image = ShiftScaleIntensity(output_min=input_min, output_max=input_max, input_min=self.output_min, input_max=self.output_max,
                                                seed=self.seed,
                                                legacy_random_state=self.legacy_random_state, *args, **kwargs)


        scaled_shifted_image = shift_scale_image(image, *args, **kwargs)

        return scaled_shifted_image





if __name__ == '__main__':



    image_input = sitk.ReadImage(r'G:\test_images\verse818_image_new.nii.gz')

    scale_gamma_intensity = ScaleGammaIntensity(min_random_gamma=0.9, max_random_gamma=1.1, output_min=0, output_max=1)

    image_output = scale_gamma_intensity(image_input)

    sitk.WriteImage(image_output, r'G:\test_images\verse818_image_new_scaled_gamma.nii.gz')



