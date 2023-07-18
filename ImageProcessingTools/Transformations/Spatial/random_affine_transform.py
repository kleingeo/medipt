from abc import ABC, abstractmethod
from typing import Union, Tuple, List
from Utils import random_uniform_float
import SimpleITK as sitk

import numpy as np

from .spatial_transform import SpatialTransform



class RandomAffineTransform(SpatialTransform):

    def __init__(self,
                 used_dimensions: bool = None,
                 dim: int = 3,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,

                 *args, **kwargs
                 ):


        super(RandomAffineTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)


        self.min_range = None
        self.max_range = None



    def _get_random_transform(self,
                              min_range: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray],
                              max_range: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray],
                              value_offset: Union[int, float] = None,
                              transform_dict: dict = None,
                              *args, **kwargs):

        self.min_range = min_range
        self.max_range = max_range


        if isinstance(min_range, (tuple, list, np.ndarray)):
            assert isinstance(self.max_range, (tuple, list, np.ndarray)), 'both min and max angles must be tuples, lists or np.ndarrays.'

            if len(self.min_range) > 1 or len(self.max_range) > 1:
                assert len(self.min_range) == self.dim, f'min angles must be a tuple or list of length {self.dim}.'
                assert len(self.max_range) == self.dim, f'max angles must be a tuple or list of length {self.dim}.'

                random_params = random_uniform_float(self.min_range, self.max_range,
                                                     seed=self.seed, legacy_random_state=self.legacy_random_state)
            else:
                random_params = random_uniform_float(self.min_range[0], self.max_range[0], output_size=self.dim,
                                                     seed=self.seed, legacy_random_state=self.legacy_random_state)


        elif isinstance(self.min_range, (int, float, np.ndarray, np.float_, np.int_)):
            assert isinstance(self.max_range, (int, float, np.ndarray, np.float_, np.int_)), 'both min and max rotations must be numbers.'

            random_params = random_uniform_float(self.min_range, self.max_range, output_size=self.dim,
                                                 seed=self.seed, legacy_random_state=self.legacy_random_state)

        else:
            raise ValueError('min and max offsets must be tuples, lists, or numbers.')


        if value_offset is not None:
            if isinstance(random_params, (list, tuple)):
               random_params = [x + value_offset for x in random_params]
            elif isinstance(random_params, np.ndarray):
                random_params += value_offset

        self.t = self.get_transform(random_params, *args, **kwargs)

        return self.t
