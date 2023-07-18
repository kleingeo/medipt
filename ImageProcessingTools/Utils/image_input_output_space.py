import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple, List

from ImageProcessingTools.Transformations import get_output_size_from_spacing, get_output_spacing_from_size



def resolve_input_output_space(
        dim: int = 3,
        input_image: sitk.Image = None,
        reference_image: sitk.Image = None,
        input_size: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        output_size: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        input_spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,

        output_spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        input_direction: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        output_direction: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        input_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        output_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
        *args, **kwargs):


    if input_image is not None:
        input_size = input_image.GetSize()
        input_spacing = input_image.GetSpacing()
        input_origin = input_image.GetOrigin()
        input_direction = input_image.GetDirection()

    else:
        input_size = kwargs.get('input_size', input_size)
        input_spacing = kwargs.get('input_spacing', input_spacing)
        input_origin = kwargs.get('input_origin', input_origin)
        input_direction = kwargs.get('input_direction', input_direction)

        if input_spacing is None:
            input_spacing = [1.0] * dim

        if input_origin is None:
            input_origin = [0] * dim

        if input_direction is None:
            input_direction = np.eye(dim).flatten().tolist()

    if reference_image is not None:
        output_size = reference_image.GetSize()
        output_direction = reference_image.GetDirection()
        output_origin = reference_image.GetOrigin()
        output_spacing = reference_image.GetSpacing()
    else:
        output_size = kwargs.get('output_size', output_size)
        output_spacing = kwargs.get('output_spacing', output_spacing)
        output_origin = kwargs.get('output_origin', output_origin)
        output_direction = kwargs.get('output_direction', output_direction)


    if (output_size is None) and (output_spacing is None) and (input_image is None):
        raise ValueError('One of output_size, output_spacing or input_image must be provided.')

    if output_direction is None:
        output_direction = input_direction

    if output_origin is None:
        output_origin = input_origin

    if (output_size is None) and (output_spacing is not None):
        output_size = get_output_size_from_spacing(dim=dim,
                                                   input_size=input_size,
                                                   input_spacing=input_spacing,
                                                   input_direction=input_direction,
                                                   output_spacing=output_spacing,
                                                   output_direction=output_direction,
                                                   *args, **kwargs)

        output_size = [int(np.round(x)) for x in output_size]

    elif (output_size is not None) and (output_spacing is None):
        output_spacing = get_output_spacing_from_size(dim=dim,
                                                      input_size=input_size,
                                                      input_spacing=input_spacing,
                                                      input_direction=input_direction,
                                                      output_size=output_size,
                                                      output_direction=output_direction,
                                                      *args, **kwargs)



    elif (output_spacing is None) and (output_size is None):
        output_spacing = input_spacing
        output_size = input_size

    kwargs['input_image'] = input_image
    kwargs['input_size'] = input_size
    kwargs['input_spacing'] = input_spacing
    kwargs['input_origin'] = input_origin
    kwargs['input_direction'] = input_direction

    kwargs['output_size'] = output_size
    kwargs['output_spacing'] = output_spacing
    kwargs['output_origin'] = output_origin
    kwargs['output_direction'] = output_direction

    return kwargs



if __name__ == '__main__':


    dim = 3

    input_image = sitk.ReadImage('../../sub-verse260.nii.gz')

    output_size = [256, 256, 256]
    output_spacing = [3.0, 5.0, 2.0]

    hold = resolve_input_output_space(dim=dim,
                                      input_image=input_image,
                                      output_size=output_size,
                                      # output_spacing=output_spacing,                               )
                                      )


