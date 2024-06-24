from abc import ABC
from typing import Union, Tuple, List
from types import ModuleType
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform
from .random_affine_transform import RandomAffineTransform


class RotationTransform(SpatialTransform):
    """
    Rotation transformation base class.
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
    #
    #     super(RotationTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, rand_init, *args, **kwargs)


    def _get_transform(self,
                       angles: Union[List[float], Tuple[float, ...], float],
                       *args, **kwargs):

        """
        Returns the sitk transform based on the given parameters.
        :param dim: The dimension.
        :param angles: List of angles for each dimension (in radians).
        :return: The sitk.AffineTransform().
        """
        if not isinstance(angles, (list, tuple)):
            angles = [angles]
        assert isinstance(angles, (list, tuple)), 'Angles parameter must be a list of floats, one for each dimension.'

        assert len(angles) in [1, self.dim], 'Angles must be a list of length 1 for 2D, or 3 for 3D.'

        self.transform = sitk.AffineTransform(self.dim)

        if isinstance(angles, (tuple, list)):

            if len(angles) == 1:
                # 2D
                self.transform.Rotate(0, 1, angle=angles[0])

            elif len(angles) > 1:
                assert len(angles) == self.dim, f'angles must be a list of length {self.dim}.'

                # 3D
                # rotate about x axis
                self.transform.Rotate(1, 2, angle=angles[0])
                # rotate about y axis
                self.transform.Rotate(0, 2, angle=angles[1])
                # rotate about z axis
                self.transform.Rotate(0, 1, angle=angles[2])


        elif isinstance(angles, (int, float, np.ndarray)):
            self.transform.Rotate(0, 1, angle=angles)

        # return self.t

        a = 1


    def get_transform(self,
                      angles: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs):

        self._get_transform(angles, *args, **kwargs)

        # return t

class RandomRotation(RotationTransform, RandomAffineTransform):
    """
    A rotation transformation with random angles (in radian).
    """
    # def __init__(self,
    #              dim: int,
    #              used_dimensions: bool = None,
    #              # min_angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray, None] = None,
    #              # max_angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray, None] = None,
    #
    #              seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
    #              legacy_random_state: bool = True,
    #
    #              *args, **kwargs):
    #     """
    #     Initializer.
    #     :param dim: The dimension.
    #     :param random_angles: List of random angles per dimension. Random angle is calculated uniformly within [-random_angles[i], random_angles[i]]
    #     :param args: Arguments passed to super init.
    #     :param kwargs: Keyword arguments passed to super init.
    #     """
    #
    #
    #     super(RandomRotation, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)




    def get_random_transform(self,
                             min_angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray, None] = None,
                             max_angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray, None] = None,
                             transformation_dict: dict = None,
                             *args, **kwargs):


        self._get_random_transform(min_angles, max_angles, transformation_dict=transformation_dict, *args, **kwargs)



