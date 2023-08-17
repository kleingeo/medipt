import numpy as np
from ...utils import random_uniform_float
from typing import Union, Tuple, List

def change_gamma_unnormalized(img, l):
    min_value = np.min(img)
    max_value = np.max(img)
    input_range = (min_value, max_value)
    range_0_1 = (0, 1)
    normalized = scale(img, input_range, range_0_1)
    normalized = change_gamma(normalized, l)
    return scale(normalized, range_0_1, input_range)


def change_gamma(img, l):
    return np.power(img, l)


def scale(img, old_range, new_range):
    shift = -old_range[0] + new_range[0] * (old_range[1] - old_range[0]) / (new_range[1] - new_range[0])
    scale = (new_range[1] - new_range[0]) / (old_range[1] - old_range[0])
    return (img + shift) * scale



def random_change_gamma(img, lambda_min=0.5, lambda_max=1.5,
                        seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                        legacy_random_state: bool = True):

    l = random_uniform_float(lambda_min, lambda_max,
                             seed=seed,
                             legacy_random_state=legacy_random_state)
    return change_gamma_unnormalized(img, l)