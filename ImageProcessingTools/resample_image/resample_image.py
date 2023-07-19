import numpy as np
import SimpleITK as sitk
from typing import Union, Tuple, List, Callable, Iterable


def get_sitk_interpolator(interpolator):
    """
    Return an sitk interpolator object for the given string.

    :param interpolator: Interpolator type as string.
                         'nearest': sitk.sitkNearestNeighbor
                         'linear': sitk.sitkLinear
                         'cubic': sitk.sitkBSpline
                         'label_gaussian': sitk.sitkLabelGaussian
                         'gaussian': sitk.sitkGaussian
                         'lanczos': sitk.sitkLanczosWindowedSinc
    :return: The sitk interpolator object.

    """

    if isinstance(interpolator, str):

        if interpolator == 'nearest':
            return sitk.sitkNearestNeighbor
        elif interpolator == 'linear':
            return sitk.sitkLinear
        elif interpolator == 'cubic':
            return sitk.sitkBSpline
        elif interpolator == 'label_gaussian':
            return sitk.sitkLabelGaussian
        elif interpolator == 'gaussian':
            return sitk.sitkGaussian
        elif interpolator == 'lanczos':
            return sitk.sitkLanczosWindowedSinc

    elif isinstance(interpolator, int):
        return interpolator

    else:
        raise Exception('invalid interpolator type')





class ResampleImage:
    def __init__(self,

                 interpolator: Union[str, int] = 'linear',


                 post_processing_sitk: Union[Callable, Union[List[Callable]], Tuple[Callable, ...]] = None,

                 np_pixel_type: Union[str, type] = np.float32,
                 default_pixel_value: Union[float, int, None] = None,

                 dim: int = 3,
                 used_dimensions: bool = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):



        self.used_dimensions = used_dimensions or [True] * dim
        self.dim = dim

        self.seed = seed
        self.legacy_random_state = legacy_random_state


        self.interpolator = interpolator
        self.post_processing_sitk = post_processing_sitk
        self.np_pixel_type = np_pixel_type
        self.default_pixel_value = default_pixel_value


    def resample_image(self,
                       image: sitk.Image,
                       input_output_space_dict: dict,
                       reference_image: sitk.Image = None,
                       transform: sitk.Transform = None,
                       *args, **kwargs) -> sitk.Image:

        # if image is None:
        #     image = input_output_space_dict.get('input_image', None)
        #     if image is None:
        #         image = input_output_space_dict.get('image', None)
        #         if image is None:
        #             raise Exception('No image was provided.')

        output_size = input_output_space_dict['output_size']
        output_spacing = input_output_space_dict['output_spacing']
        output_origin = input_output_space_dict['output_origin']
        output_direction = input_output_space_dict['output_direction']

        sitk_interpolator = get_sitk_interpolator(self.interpolator)

        if self.default_pixel_value is None:
            default_value_filter = sitk.MinimumMaximumImageFilter()
            default_value_filter.Execute(image)
            default_pixel_value = default_value_filter.GetMinimum()
        else:
            default_pixel_value = self.default_pixel_value

        resample_filter = sitk.ResampleImageFilter()

        if reference_image is not None:
            resample_filter.SetReferenceImage(reference_image)

        else:
            resample_filter.SetOutputSpacing(output_spacing)
            resample_filter.SetOutputOrigin(output_origin)
            resample_filter.SetOutputDirection(output_direction)
            resample_filter.SetSize(output_size)

        resample_filter.SetDefaultPixelValue(default_pixel_value)

        if transform is None:
            resample_filter.SetTransform(sitk.AffineTransform(self.dim))

        else:
            resample_filter.SetTransform(transform)

        resample_filter.SetInterpolator(sitk_interpolator)

        resampled_image = resample_filter.Execute(image)

        return resampled_image



    def get_images(self,
                   images: Union[List[sitk.Image], Tuple[sitk.Image, ...], sitk.Image],
                   input_output_space_dict: dict,

                   reference_image: sitk.Image = None,
                   transform: sitk.Transform = None,
                   *args, **kwargs
                   ):


        if isinstance(images, (list, tuple)):
            return [self.resample_image(image, input_output_space_dict, reference_image, transform, *args, **kwargs) for image in images]

        else:
            return self.resample_image(images, input_output_space_dict, reference_image, transform, *args, **kwargs)

    def get_resampled_images(self,
                             image: Union[List[sitk.Image], Tuple[sitk.Image, ...], sitk.Image],
                             input_output_space_dict: dict,
                             reference_image: sitk.Image = None,
                             transform: sitk.Transform = None,
                             *args, **kwargs
                             ) -> Union[List[sitk.Image], Tuple[sitk.Image, ...], sitk.Image]:

        output_image_sitk = self.get_resampled_images(image, input_output_space_dict,
                                                      reference_image, transform,
                                                      *args, **kwargs)

        if self.post_processing_sitk is not None:
            if isinstance(self.post_processing_sitk, (list, tuple)):
                for post_processing_sitk in self.post_processing_sitk:
                    output_image_sitk = post_processing_sitk(output_image_sitk)

            else:
                output_image_sitk = self.post_processing_sitk(output_image_sitk)


        return output_image_sitk