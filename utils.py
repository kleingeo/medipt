
import numpy as np


class SpatialTransformBase:
    """
    A generic spatial transform that can be applied to 2D and 3D images.
    """
    # def __init__(self, dim, *args, **kwargs):
    #     """
    #     Initializer.
    #     :param dim: The dimension of the transformation.
    #     :param args: Arguments passed to super init.
    #     :param kwargs: Keyword arguments passed to super init.
    #     """
    #     self.dim = dim

    def get_input_params(self, input_image=None,
                         input_size=None, input_spacing=None,
                         input_direction=None, input_origin=None, **kwargs):

        input_size, input_spacing, input_origin, input_direction = self.get_image_parameters(
            image=input_image,
            input_size=input_size,
            input_spacing=input_spacing,
            input_direction=input_direction,
            input_origin=input_origin
        )

        return input_size, input_spacing, input_origin, input_direction

    def get_output_params(self, input_image=None,
                          output_size=None, output_spacing=None,
                          output_direction=None, output_origin=None, **kwargs):

        assert (output_size is not None) or (output_spacing is not None) or (input_image is not None), 'One must exist.'

        if output_spacing is not None:
            dim = len(output_spacing)
        if output_size is not None:
            dim = len(output_size)

        if input_image is not None:
            input_size, input_spacing, input_origin, input_direction = self.get_image_parameters(image=input_image)
        else:
            input_size = None
            input_spacing = None
            input_origin = [0] * dim
            input_direction = np.eye(dim).flatten().tolist()

        if output_origin is None:
            output_origin = input_origin

        if output_direction is None:
            output_direction = input_direction

        if (output_spacing is not None) and (output_size is None):
            output_size = [int(input_size[idx] * input_spacing[idx] / output_spacing[idx]) for idx in range(dim)]
        elif (output_spacing is None) and (output_size is not None):
            output_spacing = [int(input_size[idx] * input_spacing[idx] / output_size[idx]) for idx in range(dim)]
        elif (output_spacing is None) and (output_size is None):
            output_spacing = input_spacing
            output_size = input_size

        return output_size, output_spacing, output_origin, output_direction

    @staticmethod
    def get_image_parameters(image=None,
                             input_size=None,
                             input_spacing=None,
                             input_direction=None,
                             input_origin=None, **kwargs):

        if image:
            input_size = image.GetSize()
            input_spacing = image.GetSpacing()
            input_origin = image.GetOrigin()
            input_direction = image.GetDirection()

        else:
            input_size = input_size
            input_spacing = input_spacing
            input_origin = input_origin
            input_direction = input_direction

        return input_size, input_spacing, input_origin, input_direction


def image_center(input_size, **kwargs):
    """
    Returns the input center based on either the parameters defined by the initializer or by **kwargs.
    The function uses the result of self.get_image_size_spacing_direction_origin(**kwargs) to define the output_center for each entry of output_size and output_spacing that is None.
    :param kwargs: Must contain either 'image', or 'input_size' and 'input_spacing', which define the input image physical space.
    :return: The sitk.AffineTransform().
    """
    # -1 is important, as it is always the center pixel.
    input_size_half = [(size - 1) * 0.5 for size in input_size]
    return input_size_half
    # return index_to_physical_point(input_size_half, input_origin, input_spacing, input_direction)


def output_image_center(dim, output_size=None, output_spacing=None, output_origin=None, output_direction=None, **kwargs):
    """
    Returns the output center based on either the parameters defined by the initializer or by **kwargs.
    The function uses the result of self.get_image_size_spacing(**kwargs) to define the output_center for each entry of output_size and output_spacing that is None.
    :param kwargs: If it contains output_size or output_spacing, use them instead of self.output_size or self.output_spacing. Otherwise, the parameters given to self.get_image_size_spacing(**kwargs).
    :return: List of output center coordinate for each dimension.
    """

    if output_spacing is None:
        output_spacing = [1] * dim

    if output_origin is None:
        output_origin = [0] * dim

    if output_direction is None:
        output_direction = np.eye(dim).flatten().tolist()


    output_size = kwargs.get('output_size', list(output_size).copy())
    output_spacing = kwargs.get('output_spacing', list(output_spacing).copy())
    output_origin = kwargs.get('output_origin', list(output_origin).copy())
    output_direction = kwargs.get('output_direction', list(output_direction).copy())

    if not all(output_size):
        # TODO check, if direction or origin are needed
        input_size, input_spacing, input_direction, input_origin = image_params(**kwargs)
    else:
        input_size, input_spacing = None, None

    if output_size is None:
        # -1 is important, as it is always the center pixel.
        output_center = (np.array(input_size) - 1) * np.array(input_spacing) * 0.5
    else:
        # -1 is important, as it is always the center pixel.

        mid_index_out = (np.array(output_size) - 1) / 2

        output_center = np.array(output_origin) + np.matmul(np.matmul(np.array(output_direction).reshape([dim, dim]), np.diag(output_spacing)), np.array(mid_index_out))
    return list(output_center)


def image_params(image=None,
                 image_spacing=None, image_size=None,
                 image_origin=None, image_direction=None, **kwargs):
    """
    Returns a tuple of (input_size, input_spacing) that is defined by the current kwargs.
    :param kwargs: The current image arguments. Either 'image', or 'input_size' and 'input_spacing'
                   'image': sitk image from which the size and spacing will be read.
                   'input_size': Input size tuple.
                   'input_spacing': Input spacing tuple.
                   'input_origin': Input origin tuple.
    :return: (input_size, input_spacing, input_origin) tuple.
    """
    if image:
        image_size = image.GetSize()
        image_spacing = image.GetSpacing()
        image_direction = image.GetDirection()
        image_origin = image.GetOrigin()
        return image_size, image_spacing, image_direction, image_origin
    else:
        image_size = image_size
        image_spacing = image_spacing
        image_direction = image_direction
        image_origin = image_origin
        return image_size, image_spacing, image_direction, image_origin



def index_to_physical_point(index, origin, spacing, direction):
    """
    Returns a physical point for an image index and given image metadata.
    :param index: The index to transform.
    :param origin: The image origin.
    :param spacing: The image spacing.
    :param direction: The image direction.
    :return: The transformed point.
    """
    dim = len(index)
    physical_point = np.array(origin) + np.matmul(np.matmul(np.array(direction).reshape([dim, dim]), np.diag(spacing)), np.array(index))
    return list(physical_point)


def physical_point_to_index(point, origin, spacing, direction):
    """
    Returns an image index for a physical point and given image metadata.
    :param point: The point to transform.
    :param origin: The image origin.
    :param spacing: The image spacing.
    :param direction: The image direction.
    :return: The transformed point.
    """
    dim = len(point)
    index = np.matmul(np.matmul(np.diag(1 / np.array(spacing)), np.array(direction).reshape([dim, dim]).T), (np.array(point) - np.array(origin)))
    return index.tolist()
