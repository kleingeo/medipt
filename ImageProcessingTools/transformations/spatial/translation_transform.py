from typing import Union, Tuple, List
from ImageProcessingTools.utils import random_uniform_float
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform
from .random_affine_transform import RandomAffineTransform
from ImageProcessingTools.transformations import physical_image_size



class TranslateTransform(SpatialTransform):
    """
    Translation transformation base class.
    """
    def __init__(self,
                 dim: int = 3,
                 used_dimensions: bool = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):
        """
        Initializer
        :param dim: The dimension.
        :param used_dimensions: Boolean list of which dimension indizes to use for the transformation.
        :param args: Arguments passed to super init.
        :param kwargs: Keyword arguments passed to super init.
        """

        super(TranslateTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)

        assert len(self.used_dimensions) == dim, 'Length of used_dimensions must be equal to dim.'

    def _get_transform(self,
                      translation: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs):
        """
        Returns the sitk transform based on the given parameters.
        :param dim: The dimension.
        :param offset: List of offsets for each dimension.
        :return: The sitk.AffineTransform().
        """

        assert len(translation) == self.dim, 'Length of offset must be equal to dim.'

        t = sitk.AffineTransform(self.dim)
        t.Translate(translation)
        return t


class RandomTranslation(RandomAffineTransform, TranslateTransform):
    """
    A translation transformation with a random offset.
    """
    def __init__(self,
                 # min_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray],
                 # max_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray],
                 dim: Union[int, None] = 3,
                 used_dimensions: bool = None,

                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):
        """
        Initializer.
        :param dim: The dimension.
        :param random_offset: List of random offsets per dimension. Random offset is calculated uniformly within [-random_offset[i], random_offset[i]]
        :param args: Arguments passed to super init.
        :param kwargs: Keyword arguments passed to super init.
        """

        super(RandomTranslation, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)

    def get_random_transform(self,
                             min_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray],
                             max_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray],
                             transformation_dict, *args, **kwargs):


        self.transform = self._get_random_transform(min_trans, max_trans, transformation_dict, *args, **kwargs)

        # return self.transform



class TranslateInputOriginToInputCenter(TranslateTransform):
    def get_transform(self,
                      *args, **kwargs):

        input_center_phys = self.get_input_center(*args, **kwargs)
        input_origin_phys = self.get_input_origin(*args, **kwargs)

        translation = tuple([input_origin_phys[i] - input_center_phys[i] for i in range(self.dim)])

        self.transform = self._get_transform(translation)

        # return self.t

class TranslateOutputOriginToOutputCenter(TranslateTransform):
    def get_transform(self,
                      *args, **kwargs):

        output_center_phys = self.get_output_center(*args, **kwargs)
        output_origin_phys = self.get_output_origin(*args, **kwargs)

        translation = tuple([output_origin_phys[i] - output_center_phys[i] for i in range(self.dim)])

        self.transform = self._get_transform(translation)

        # return self.t





class RandomFactorInput(TranslateTransform):
    """
    A translation transform that translates the input image by a random factor, such that it will be cropped.
    The input center should usually be at the origin before this transformation.
    The actual translation value per dimension will be calculated as follows:
    (input_size[i] * input_spacing[i] - self.remove_border[i]) * float_uniform(-self.random_factor[i], self.random_factor[i]) for each dimension.
    """
    def get_transform(self,
                      random_factor,
                      remove_border=None,
                      *args, **kwargs):
        """
        Returns the sitk transform based on the given parameters.
        :param kwargs: Must contain either 'image', or 'input_size' and 'input_spacing', which define the input image physical space.
        :return: The sitk.AffineTransform().
        """

        # TODO check to see if this works for arbitrary input directions and origins


        remove_border = remove_border or [0.0] * self.dim

        self.get_input_output_space(*args, **kwargs)

        # assert np.allclose(self.input_direction, np.eye(self.dim).flatten()), 'this transformation only works for eye direction, is: ' + self.input_direction
        # assert np.allclose(self.input_origin, np.zeros(self.dim)), 'this transformation only works for zeros origin, is: ' + self.input_origin


        phys_input_size = physical_image_size(dim=self.dim,
                                              size=self.input_size,
                                              spacing=self.input_spacing,
                                              direction=self.input_direction)

        phys_input_size = np.array(phys_input_size) - np.array(remove_border)

        random_factor = np.array(random_factor)

        random_scaling = np.array(random_uniform_float(low_value=-random_factor, high_value=random_factor,
                                                       output_size=self.dim,
                                                       seed=self.seed, legacy_random_state=self.legacy_random_state))

        translation = list(phys_input_size * random_scaling)

        self.transform = self._get_transform(translation)

        # return self.t
