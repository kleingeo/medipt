import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple, List
from imageprocessingtools.utils import random_uniform_float


def rotation_transform(angles: Union[tuple, list], dim: int = 3):
    '''

    :param angles:
    :param dim:
    :return: sitk.AffineTransform
    '''

    t = sitk.AffineTransform(dim)

    if isinstance(angles, (tuple, list)):

        if len(angles) == 1:
            # 2D
            t.Rotate(0, 1, angle=angles[0])

        elif len(angles) > 1:
            assert len(angles) == dim, f'angles must be a list of length {dim}.'

            # 3D
            # rotate about x axis
            t.Rotate(1, 2, angle=angles[0])
            # rotate about y axis
            t.Rotate(0, 2, angle=angles[1])
            # rotate about z axis
            t.Rotate(0, 1, angle=angles[2])


    elif isinstance(angles, (int, float, np.ndarray)):
        t.Rotate(0, 1, angle=angles)

    return t



def random_rotation(angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray, None] = None,
                    min_angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray, None] = None,
                    max_angles: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.int_, np.float_, np.ndarray, None] = None,
                    dim: int = 3,

                    seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                    legacy_random_state: bool = True,
                    ):

    if angles is not None:
        if isinstance(angles, (tuple, list)):
            min_angles = [-1 * a for a in angles]
            max_angles = angles


        elif isinstance(angles, (int, float, np.int_, np.float_, np.ndarray)):
            min_angles = -1 * angles
            max_angles = angles

        else:
            raise ValueError('angles must be a number, or a tuple or list of numbers.')




    if isinstance(min_angles, (tuple, list, np.ndarray)):
        assert isinstance(max_angles, (tuple, list, np.ndarray)), 'both min and max angles must be tuples, lists or np.ndarrays.'

        if len(min_angles) > 1 or len(max_angles) > 1:
            assert len(min_angles) == dim, f'min angles must be a tuple or list of length {dim}.'
            assert len(max_angles) == dim, f'max angles must be a tuple or list of length {dim}.'

            random_rotation = random_uniform_float(min_angles, max_angles)
        else:
            random_rotation = random_uniform_float(min_angles[0], max_angles[0], output_size=dim)


    elif isinstance(min_angles, (int, float, np.ndarray, np.float_, np.int_)):
        assert isinstance(max_angles, (int, float, np.ndarray, np.float_, np.int_)), 'both min and max rotations must be numbers.'

        random_rotation = random_uniform_float(min_angles, max_angles, output_size=dim)

    else:
        raise ValueError('min and max offsets must be tuples, lists, or numbers.')


    t = rotation_transform(random_rotation)

    return t

    # if isinstance(min_angles, (tuple, list, np.ndarray)):
    #
    #     assert len(min_angles) == dim, f'min angles must be a tuple or list of length {dim}.'
    #     assert len(max_angles) == dim, f'max angles must be a tuple or list of length {dim}.'
    #
    #     assert isinstance(max_angles, (tuple, list)), 'both min and max angles must be tuples or lists.'
    #
    #     random_rotation = [float(np.random.uniform(min_value, max_value))
    #                        for min_value, max_value in zip(min_angles, max_angles)]
    #
    #     random_rotation = random_uniform_float(min_angles, max_angles)
    #
    # elif isinstance(min_angles, (int, float, np.ndarray, np.float_, np.int_)):
    #     assert isinstance(max_angles, (int, float, np.ndarray, np.float_, np.int_)), 'both min and max offsets must be numbers.'
    #
    #     # random_rotation = [float(np.random.uniform(min_angles, max_angles)) for _ in range(dim)]
    #
    # else:
    #     raise ValueError('min and max offsets must be tuples, lists, or numbers.')
    #
    # t = rotation_transform(random_rotation)
    #
    # return t