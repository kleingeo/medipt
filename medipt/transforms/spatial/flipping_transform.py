from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform
from ...utils import random_binomial


class FlippingTransform(SpatialTransform):

    def _get_transform(self,
                       flip_axes: Union[List[float], Tuple[float, ...], float],
                       *args, **kwargs):



        if isinstance(flip_axes, (tuple, list, np.ndarray)):
            current_flip_axes = []
            if len(flip_axes) > 1:
                if len(flip_axes) != self.dim:
                    raise ValueError(f'flip axes must be a tuple or list of length {self.dim}.')

            for flip_axis in flip_axes:

                current_flip_axes.append(bool(flip_axis))

        elif isinstance(flip_axes, (int, float, np.integer, np.floating, np.bool_, bool)):
            current_flip_axes = [bool(flip_axes)] * self.dim

        else:
            raise ValueError('flip axes must be tuples, lists, or numbers.')



        self.transform = sitk.AffineTransform(self.dim)

        scale_factors = [-1.0 if f else 1.0 for f in current_flip_axes]

        self.transform.Scale(scale_factors)

    def get_transform(self,
                      flip_axes: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs
                      ):

        self._get_transform(flip_axes, *args, **kwargs)



class RandomFlipping(FlippingTransform):

    def get_random_transform(self,
                             flip_axes: Union[
                                 List[Union[int, float, bool]],
                                 Tuple[Union[int, float, bool], ...],
                                 Union[int, float, bool, np.integer, np.floating],
                                 np.ndarray],
                             *args, **kwargs,
                             ):

        if isinstance(flip_axes, (tuple, list, np.ndarray)):

            if isinstance(flip_axes, np.ndarray):
                probability = flip_axes * 0.5

            elif isinstance(flip_axes, (list, tuple)):
                probability = 0.5 * np.array(flip_axes)

            else:
                raise ValueError('flip axes must be tuples, lists, or numbers.')

        elif isinstance(flip_axes, (int, float, np.integer, np.floating, np.bool_, bool)):

            probability = 0.5 * flip_axes

        else:
            raise ValueError('flip axes must be tuples, lists, or numbers.')

        current_flip_axis = random_binomial(n=1, p=probability,
                                            seed=self.seed,
                                            legacy_random_state=self.legacy_random_state,
                                            rand_init=self.rand_init)

        self._get_transform(current_flip_axis, *args, **kwargs)









        #
        # if isinstance(flip_axes, (tuple, list, np.ndarray)):
        #     current_flip_axes = []
        #     if len(flip_axes) > 1:
        #         if len(flip_axes) != self.dim:
        #             raise ValueError(f'flip axes must be a tuple or list of length {self.dim}.')
        #
        #     for flip_axis in flip_axes:
        #
        #         if flip_axis == 1:
        #             current_flip_axis = random_binomial(n=1, p=0.5,
        #                                                 seed=self.seed,
        #                                                 legacy_random_state=self.legacy_random_state,
        #                                                 rand_init=self.rand_init)
        #         else:
        #             current_flip_axis = 0
        #
        #         current_flip_axes.append(bool(current_flip_axis))
        #
        # elif isinstance(flip_axes, (int, float, np.integer, np.floating, np.bool_, bool)):
        #     if flip_axes == 1:
        #         current_flip_axis = random_binomial(n=1, p=0.5,
        #                                             seed=self.seed,
        #                                             legacy_random_state=self.legacy_random_state,
        #                                             rand_init=self.rand_init)
        #
        #     else:
        #         current_flip_axis = 0
        #     current_flip_axes = [bool(current_flip_axis)] * self.dim
        #
        # else:
        #     raise ValueError('flip axes must be tuples, lists, or numbers.')
        #
        # self._get_transform(current_flip_axes, *args, **kwargs)
