from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform
from .random_affine_transform import RandomAffineTransform
from ImageProcessingTools.Utils import random_binomial


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

        elif isinstance(flip_axes, (int, float, np.int_, np.float_, np.bool_, bool)):
            current_flip_axes = [bool(flip_axes)] * self.dim

        else:
            raise ValueError('flip axes must be tuples, lists, or numbers.')






        # if isinstance(flip_axes, (tuple, list, np.ndarray)):
        #
        #     if len(flip_axes) == 1:
        #         current_flip_axes = [flip_axes] * self.dim
        #
        #     else:
        #         assert len(flip_axes) == self.dim, f'flip axes must be a tuple or list of length {self.dim}.'
        #
        #         current_flip_axes = [flip_axes]
        #
        # elif isinstance(flip_axes, (int, float, np.ndarray)):
        #     current_flip_axes = [flip_axes] * self.dim
        #
        # else:
        #     raise ValueError('flip axes must be tuples, lists, or numbers.')

        self.transform = sitk.AffineTransform(self.dim)

        scale_factors = [-1.0 if f else 1.0 for f in current_flip_axes]

        self.transform.Scale(scale_factors)

    def get_transform(self,
                      flip_axes: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs
                      ):

        self._get_transform(flip_axes, *args, **kwargs)



class RandomFlippingTransform(FlippingTransform):

    def get_random_transform(self,
                             flip_axes: Union[
                                 List[Union[int, float, bool]],
                                 Tuple[Union[int, float, bool], ...],
                                 Union[int, float, bool, np.int_, np.float_],
                                 np.ndarray],
                             *args, **kwargs,
                             ):



        if isinstance(flip_axes, (tuple, list, np.ndarray)):
            current_flip_axes = []
            if len(flip_axes) > 1:
                if len(flip_axes) != self.dim:
                    raise ValueError(f'flip axes must be a tuple or list of length {self.dim}.')

            for flip_axis in flip_axes:

                if flip_axis == 1:
                    current_flip_axis = random_binomial(n=1, p=0.5,
                                                        seed=self.seed,
                                                        legacy_random_state=self.legacy_random_state)
                else:
                    current_flip_axis = 0

                current_flip_axes.append(bool(current_flip_axis))

        elif isinstance(flip_axes, (int, float, np.int_, np.float_, np.bool_, bool)):
            if flip_axes == 1:
                current_flip_axis = random_binomial(n=1, p=0.5,
                                                    seed=self.seed,
                                                    legacy_random_state=self.legacy_random_state)

            else:
                current_flip_axis = 0
            current_flip_axes = [bool(current_flip_axis)] * self.dim

        else:
            raise ValueError('flip axes must be tuples, lists, or numbers.')



        self.transform = sitk.AffineTransform(self.dim)

        scale_factors = [-1.0 if f else 1.0 for f in current_flip_axes]

        self.transform.Scale(scale_factors)
