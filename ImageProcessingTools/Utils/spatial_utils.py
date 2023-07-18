import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple, List


def image_center(input_size: Tuple[int, ...],
                 *args, **kwargs):

    # -1 is important, as it is always the center pixel.
    input_size_half = [(size - 1) * 0.5 for size in input_size]
    return input_size_half


def physical_image_size(dim: int,
                        size: Tuple[int, ...],
                        spacing: Tuple[float, ...],
                        direction: Tuple[float, ...],
                        *args, **kwargs) -> List[float]:

    phys_size = np.matmul(size, np.matmul(np.array(direction).reshape([dim, dim]), np.diag(spacing)))

    return list(phys_size)



def get_output_size_from_spacing(dim: int,
                                 input_size: Union[List[int], Tuple[int, ...]],
                                 input_spacing: Union[List[int], Tuple[int, ...]],
                                 input_direction: Union[List[int], Tuple[int, ...]],
                                 output_spacing: Union[List[int], Tuple[int, ...]],
                                 output_direction: Union[List[int], Tuple[int, ...]] = None,
                                 *args, **kwargs):

    input_total_space = physical_image_size(dim=dim,
                                            size=input_size,
                                            spacing=input_spacing,
                                            direction=input_direction)

    output_direction_reshape = np.array(output_direction).reshape([dim, dim])


    out_spacing_direction = np.matmul(output_direction_reshape, np.diag(output_spacing))

    output_size = np.matmul(input_total_space, np.linalg.inv(out_spacing_direction))

    return output_size


def get_output_spacing_from_size(dim: int,
                                 input_size: Union[List[int], Tuple[int, ...]],
                                 input_spacing: Union[List[int], Tuple[int, ...]],
                                 input_direction: Union[List[int], Tuple[int, ...]],
                                 output_size: Union[List[int], Tuple[int, ...]],
                                 output_direction: Union[List[int], Tuple[int, ...]] = None,
                                 *args, **kwargs):

    input_total_space = physical_image_size(dim=dim,
                                            size=input_size,
                                            spacing=input_spacing,
                                            direction=input_direction)

    output_direction_reshape = np.array(output_direction).reshape([dim, dim])


    out_size_direction = np.matmul(np.diag(output_size), output_direction_reshape)

    output_spacing = np.matmul(np.linalg.inv(out_size_direction), input_total_space)

    return output_spacing


def image_index_to_phys(dim: int,
                        index_coords: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                        image: sitk.Image = None,
                        size: Tuple[int, ...] = None,
                        origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                        spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                        direction: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                        *args, **kwargs) -> List[float]:


    if image is not None:
        phys_coord = image.TransformContinuousIndexToPhysicalPoint(index_coords)
        return phys_coord


    if spacing is None:
        spacing = [1.0] * dim

    if origin is None:
        origin = [0] * dim

    if direction is None:
        direction = np.eye(dim).flatten().tolist()

    phys_coord = np.array(origin) + np.matmul(
        np.matmul(np.array(direction).reshape([dim, dim]), np.diag(spacing)),
        np.array(index_coords)
    )


    return list(phys_coord)



