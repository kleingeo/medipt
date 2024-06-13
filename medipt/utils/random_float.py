import numpy as np
import random
from typing import Union, Tuple, List, Any, Callable, Optional
from types import ModuleType


def initialize_rand_state(
        seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
        legacy_random_state: bool = True, ) -> Union[ModuleType, np.random.Generator, np.random.BitGenerator]:
    if seed is not None:
        if isinstance(seed, int):
            if legacy_random_state:
                np.random.seed(seed)
                random.seed(seed)

            else:
                ran_gen = np.random.default_rng(seed)
                random.seed(seed)

        elif isinstance(seed, np.random.RandomState):
            np.random.set_state(np.random.get_state())
            random.setstate(random.getstate())

        elif isinstance(seed, (np.random.Generator, np.random.BitGenerator)):
            ran_gen = np.random.default_rng(seed)

    else:
        if legacy_random_state:
            np.random.set_state(np.random.get_state())
            random.setstate(random.getstate())

        else:
            ran_gen = np.random.default_rng()

    if legacy_random_state:
        rand_init = np.random

    else:
        rand_init = ran_gen

    return rand_init


def random_binomial(
        n: Union[int, float, np.int_, np.float_],
        p: Union[int, float, np.int_, np.float_],
        output_size: Union[List[Union[int, float]], Tuple[Union[int, float]], int, float, np.int_, np.float_] = None,

        ignore_axis: Union[None, List[int], Tuple[int], int] = None,

        seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,

        legacy_random_state: bool = True,

        rand_init:  Union[ModuleType, np.random.Generator, np.random.BitGenerator] = None) -> Union[np.ndarray, int]:
    '''

    :param n:
    :param p:
    :param output_size:
    :param ignore_axis: Ignores the axis specified. If None, then no axis is ignored. Works only for 1D right now.
    :param seed:
    :param legacy_random_state:
    :return:
    '''

    if rand_init is None:
        rand_init = initialize_rand_state(seed=seed, legacy_random_state=legacy_random_state)

    binomial_out = rand_init.binomial(n=n, p=p, size=output_size)

    if (output_size is not None) and (ignore_axis is not None):
        if isinstance(ignore_axis, int):
            binomial_out[ignore_axis] = 1

        elif isinstance(ignore_axis, (list, tuple)):
            for idx in ignore_axis:
                binomial_out[idx] = 1

        else:
            raise ValueError('ignore_axis must be an int, list, or tuple.')

    return binomial_out


def random_uniform_float(
        low_value: Union[float, int, List[Union[int, float]], Tuple[Union[int, float], ...], np.int_, np.float_, np.ndarray],
        high_value: Union[float, int, List[Union[int, float]], Tuple[Union[int, float], ...], np.int_, np.float_, np.ndarray],
        output_size: Union[float, int, List[Union[int, float]], Tuple[Union[int, float], ...], np.int_, np.float_, np.ndarray, None] = None,

        dim: Union[int, None] = None,

        seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,

        legacy_random_state: bool = True,

        rand_init: Union[ModuleType, np.random.Generator, np.random.BitGenerator] = None


) -> Union[float, List[float], np.ndarray]:

    if rand_init is None:
        rand_init = initialize_rand_state(seed=seed, legacy_random_state=legacy_random_state)

    # if seed is not None:
    #     if isinstance(seed, int):
    #         if legacy_random_state:
    #             np.random.seed(seed)
    #             random.seed(seed)
    #
    #         else:
    #             ran_gen = np.random.default_rng(seed)
    #             random.seed(seed)
    #
    #     elif isinstance(seed, np.random.RandomState):
    #         np.random.set_state(np.random.get_state())
    #         random.setstate(random.getstate())
    #
    #     elif isinstance(seed, (np.random.Generator, np.random.BitGenerator)):
    #         ran_gen = np.random.default_rng(seed)
    #
    # else:
    #     if legacy_random_state:
    #         np.random.set_state(np.random.get_state())
    #         random.setstate(random.getstate())
    #
    #     else:
    #         ran_gen = np.random.default_rng()
    #
    #
    # if legacy_random_state:
    #     rand_init = np.random
    #
    # else:
    #     rand_init = ran_gen

    if (output_size is not None) and (dim is not None):
        if isinstance(output_size, (int, float, np.int_, np.float_)):

            output_size = (output_size, dim)

        elif isinstance(output_size, (list, tuple, np.ndarray)):
            output_size = *output_size, dim

        else:
            raise ValueError('output_size must be a number, list, tuple, or numpy array.')

    if isinstance(low_value, np.ndarray) or (isinstance(high_value, np.ndarray)):
        if isinstance(low_value, np.ndarray) and (isinstance(high_value, np.ndarray)):
            if low_value.shape != high_value.shape:
                raise ValueError('shape of low_value must be equal to shape of high_value.')

            else:
                if output_size is None:
                    random_uniform = [float(rand_init.uniform(low=l, high=h)) for l, h in zip(low_value, high_value)]
                    return random_uniform

                else:
                    random_uniform = rand_init.uniform(low=low_value, high=high_value, size=output_size)
                    return random_uniform


        elif isinstance(low_value, np.ndarray) and (isinstance(high_value, (int, float, np.int_, np.float_))):
            if len(low_value) > 1:
                raise ValueError('size of low_value must be equal to size of high_value.')

            else:
                low_value = low_value[0]
                random_uniform = float(rand_init.uniform(low=low_value, high=high_value))
                return random_uniform

        elif isinstance(low_value, (int, float, np.int_, np.float_)) and (isinstance(high_value, np.ndarray)):
            if len(high_value) > 1:
                raise ValueError('size of low_value must be equal to size of high_value.')
            else:
                high_value = high_value[0]
                random_uniform = float(rand_init.uniform(low=low_value, high=high_value))
                return random_uniform

            # if output_size is None:
            #     random_uniform = np.random.uniform(low=low_value, high=high_value)
            #     return random_uniform
            #
            # else:
            #     random_uniform = np.random.uniform(low=low_value, hig

    elif (isinstance(low_value, (int, float, np.int_, np.float_)) is False) and (
            isinstance(high_value, (int, float, np.int_, np.float_)) is False):
        if len(low_value) != len(high_value):
            raise ValueError('size of low_value must be equal to size of high_value.')

    elif (isinstance(low_value, (int, float, np.int_, np.float_)) is False) and (
    isinstance(high_value, (int, float, np.int_, np.float_))):
        high_value = [high_value] * len(low_value)

    elif (isinstance(low_value, (int, float, np.int_, np.float_))) and (
            isinstance(high_value, (int, float, np.int_, np.float_)) is False):
        low_value = [low_value] * len(high_value)





    else:
        random_uniform = rand_init.uniform(low=low_value, high=high_value, size=output_size)
        return random_uniform

    if output_size is None:
        random_uniform = [float(rand_init.uniform(low=l, high=h)) for l, h in zip(low_value, high_value)]
        return random_uniform

    else:
        random_uniform = np.stack(
            [rand_init.uniform(low=l, high=h, size=output_size) for l, h in zip(low_value, high_value)])

        return random_uniform

    # random_val_list = None
    # output_size_no_channel = None
    # if output_size:
    #     if len(output_size) > dim:
    #         output_size_no_channel = output_size[:dim]
    #
    # if isinstance(value, (int, float)):
    #     if output_size is not None:
    #         random_val_list = np.random.uniform(low=-value, high=value, size=output_size)
    #     else:
    #         random_val_list = list(np.random.uniform(low=-value, high=value, size=dim))
    #
    # elif isinstance(value, (tuple, list)):
    #     if isinstance(value[0], (float, int)):
    #         if len(value) == 1:
    #             if output_size is None:
    #                 random_val_list = list(np.random.uniform(low=-value[0], high=value[0], size=dim))
    #
    #             else:
    #                 random_val_list = np.zeros(tuple(output_size))
    #                 random_val_list[..., 0] = np.random.uniform(low=-value[0], high=value[0],
    #                                                             size=output_size_no_channel)
    #         elif len(value) == dim:
    #             if output_size is None:
    #                 random_val_list = [np.random.uniform(low=-val, high=val) for val in value]
    #
    #             else:
    #                 random_val_list = np.zeros(tuple(output_size))
    #                 for val_idx, val in enumerate(value):
    #                     random_val_list[..., val_idx] = np.random.uniform(low=-val, high=val,
    #                                                                       size=output_size_no_channel)
    #
    #
    #         elif len(value) == 2:
    #             if output_size is not None:
    #                 random_val_list = np.random.uniform(low=value[0], high=value[1], size=output_size)
    #             else:
    #                 random_val_list = list(np.random.uniform(low=value[0], high=value[1], size=dim))
    #
    #         elif len(value) == dim * 2:
    #             val_reshape = []
    #             counter = 0
    #             for v in value:
    #                 if counter == 0:
    #                     v_hold = []
    #                     v_hold.append(v)
    #                     counter = 1
    #                 elif counter == 1:
    #                     v_hold.append(v)
    #                     val_reshape.append(v_hold)
    #                     counter = 0
    #
    #             if output_size is None:
    #                 random_val_list = [np.random.uniform(low=val[0], high=val[1]) for val in val_reshape]
    #
    #             else:
    #                 random_val_list = np.zeros(tuple(output_size))
    #                 for val_idx, value in enumerate(value):
    #                     random_val_list[..., val_idx] = np.random.uniform(low=value[val_idx][0], high=value[val_idx][1],
    #                                                                       size=output_size_no_channel)
    #
    #     elif isinstance(value[0], (tuple, list)):
    #         random_val_list = [np.random.uniform(low=val[0], high=val[1]) for val in value]
    #
    #     elif isinstance(value[0], np.ndarray):
    #         raise ValueError('Numpy arrays are not currently supported. Please use list or tuples.')
    #     else:
    #         raise ValueError('value was found to have an incorrect shape')
    #
    #
    # elif isinstance(value, np.ndarray):
    #     raise ValueError('Numpy arrays are not currently supported. Please use list, tuples, floats or ints')
    # else:
    #     raise ValueError('value was found to have an incorrect shape')
    #
    #
    # return random_val_list
