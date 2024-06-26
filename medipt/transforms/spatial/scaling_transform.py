from typing import Union, Tuple, List
from types import ModuleType
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform
from .random_affine_transform import RandomAffineTransform


class ScalingTransform(SpatialTransform):
    """
    Scale transformation base class.
    """

    # def __init__(self,
    #              dim: int = 3,
    #              used_dimensions: bool = None,
    #              seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
    #              legacy_random_state: bool = True,
    #              rand_init: Union[ModuleType, np.random.Generator, np.random.BitGenerator] = None,
    #              *args, **kwargs):
    #     """
    #     Initializer
    #     :param dim: The dimension.
    #     :param used_dimensions: Boolean list of which dimension indizes to use for the transformation.
    #     :param args: Arguments passed to super init.
    #     :param kwargs: Keyword arguments passed to super init.
    #     """
    #
    #     super(ScalingTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, rand_init, *args, **kwargs)

    def _get_transform(self,
                      scale: Union[List[float], Tuple[float, ...], float, int],
                      *args, **kwargs):


        if isinstance(scale, (list, tuple)):
            assert len(scale) == self.dim, 'Length of scale must be equal to dim.'

        elif isinstance(scale, (float, int)):
            scale = [scale] * self.dim

        else:
            raise ValueError('Scale must be a list, tuple, float or int.')

        t = sitk.AffineTransform(self.dim)
        t.Scale(scale)

        self.transform = t

        # return t

    def get_transform(self,
                      scale: Union[List[float], Tuple[float, ...], float, int],
                      *args, **kwargs):

        self._get_transform(scale, *args, **kwargs)

    def get_scale_transform(self, dim, scale, direction) -> sitk.AffineTransform:
        """
        Returns the sitk transform based on the given parameters.
        :param dim: The dimension.
        :param scale: List of scale factors for each dimension.
        :return: The sitk.AffineTransform().
        """
        if isinstance(scale, list) or isinstance(scale, tuple):
            assert len(scale) == dim, 'Length of scale must be equal to dim.'

        s = sitk.AffineTransform(dim)
        s.Scale(scale)

        scale_matrix = np.array(s.GetMatrix()).reshape([self.dim, self.dim])

        aff_matrix = np.matmul(np.array(direction).reshape([self.dim, self.dim]), scale_matrix)
        s.SetMatrix(aff_matrix.flatten())
        return s




class RandomScaling(ScalingTransform, RandomAffineTransform):

    # def __init__(self,
    #              dim: int,
    #              used_dimensions: bool = None,
    #              seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
    #              legacy_random_state: bool = True,
    #
    #              *args, **kwargs):
    #
    #     super(RandomScaling, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)



    def get_random_transform(self,
                 min_scaling: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
                 max_scaling: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
                 transformation_dict: dict = None,
                 *args, **kwargs):


        self._get_random_transform(min_scaling, max_scaling,
                                   transform_dict=transformation_dict,
                                   value_offset=1.0,
                                   *args, **kwargs)

        # return self.t




class RandomUniformScaling(ScalingTransform, RandomAffineTransform):

    # def __init__(self,
    #              dim: int,
    #              used_dimensions: bool = None,
    #              seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
    #              legacy_random_state: bool = True,
    #
    #              *args, **kwargs):
    #
    #     super(RandomUniformScaling, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)



    def get_random_transform(
            self,
            min_scaling: Union[int, float, np.integer, np.floating, np.ndarray] = None,
            max_scaling: Union[int, float, np.integer, np.floating, np.ndarray] = None,
            transformation_dict: dict = None,
            *args, **kwargs):


        self._get_random_transform(min_scaling, max_scaling,
                                   transform_dict=transformation_dict,
                                   value_offset=1.0,
                                   uniform=True,
                                   *args, **kwargs)

        # return self.t





