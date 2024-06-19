import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple, List


def min_max_intensity_sitk(image: sitk.Image,
                           *args, **kwargs) -> Tuple[float, float]:

    min_max_filter = sitk.MinimumMaximumImageFilter()
    min_max_filter.Execute(image)

    image_min = min_max_filter.GetMinimum()
    image_max = min_max_filter.GetMaximum()

    return image_min, image_max



def clamp_intensity_sitk(image: sitk.Image,
                         window_min: Union[int, float] = None,
                         window_max: Union[int, float] = None,
                         image_min: Union[int, float] = None,
                         image_max: Union[int, float] = None,
                         *args, **kwargs) -> sitk.Image:


    if (window_min is None) and (window_max is None):
        raise ValueError('window_min and window_max cannot both be None.')

    if image_min is None or image_max is None:
        image_min_max = min_max_intensity_sitk(image)

        if image_min is None:
            image_min = image_min_max[0]
        if image_max is None:
            image_max = image_min_max[1]

    if window_min is None:
        window_min = image_min
    if window_max is None:
        window_max = image_max

    clamp_filter = sitk.ClampImageFilter()

    clamp_filter.SetLowerBound(window_min)
    clamp_filter.SetUpperBound(window_max)

    clamped_image = clamp_filter.Execute(image)

    return clamped_image



def shift_scale_intensity_sitk(image: sitk.Image,
                               shift: Union[int, float] = None,
                               scale: Union[int, float] = None,
                               *args, **kwargs) -> sitk.Image:

    shift_scale_filter = sitk.ShiftScaleImageFilter()
    shift_scale_filter.SetShift(shift)
    shift_scale_filter.SetScale(scale)
    shifted_scaled_image = shift_scale_filter.Execute(image)

    return shifted_scaled_image


def rescale_intensity_sitk(image: sitk.Image,
                           output_min: Union[int, float] = None,
                           output_max: Union[int, float] = None,
                           *args, **kwargs) -> sitk.Image:


    if (output_min is None) and (output_max is None):
        raise ValueError('Need to provide output minimum and/or output maximum.')
    else:
        image_min_max = min_max_intensity_sitk(image)
        if output_min is None:
            output_min = image_min_max[0]
        if output_max is None:
            output_max = image_min_max[1]


    # if (output_min is None) or (output_max is None):
    #     image_min_max = min_max_intensity_sitk(image)
    #     if output_min is None:
    #         output_min = image_min_max[0]
    #     if output_max is None:
    #         output_max = image_min_max[1]
    # else:
    #     raise ValueError('Need to provide output minimum and/or output maximum.')


    rescale_filter = sitk.RescaleIntensityImageFilter()
    rescale_filter.SetOutputMinimum(output_min)
    rescale_filter.SetOutputMaximum(output_max)

    rescaled_image = rescale_filter.Execute(image)

    return rescaled_image

def rescale_intensity_window_sitk(image: sitk.Image,
                           # output_min: Union[int, float] = None,
                           # output_max: Union[int, float] = None,
                           input_min: Union[int, float] = None,
                           input_max: Union[int, float] = None,
                           output_min: Union[int, float] = None,
                           output_max: Union[int, float] = None,
                           *args, **kwargs) -> sitk.Image:

    image_min_max = min_max_intensity_sitk(image)

    if input_min is None:
        input_min = image_min_max[0]

    if input_max is None:
        input_max = image_min_max[1]


    if (output_min is None) and (output_max is None):
        raise ValueError('Need to provide output minimum and/or output maximum.')
    else:
        if output_min is None:
            output_min = input_min
        if output_max is None:
            output_max = input_max




    rescale_filter = sitk.IntensityWindowingImageFilter()

    rescale_filter.SetOutputMaximum(output_max)
    rescale_filter.SetOutputMinimum(output_min)

    rescale_filter.SetWindowMaximum(input_max)
    rescale_filter.SetWindowMinimum(input_min)


    rescaled_image = rescale_filter.Execute(image)

    return rescaled_image




def gaussian_blur_sitk(image: sitk.Image,
                       sigma: Union[int, float],
                       *args, **kwargs) -> sitk.Image:

    image_default_pixel_type = image.GetPixelID()

    gaussian_filter = sitk.SmoothingRecursiveGaussianImageFilter()
    gaussian_filter.SetSigma(sigma)

    rescast_filter = sitk.CastImageFilter()
    rescast_filter.SetOutputPixelType(sitk.sitkFloat64)
    image = rescast_filter.Execute(image)

    output_image = gaussian_filter.Execute(image)

    if image_default_pixel_type != sitk.sitkFloat64:
        output_image = sitk.Cast(output_image, image_default_pixel_type)

    return output_image



def gaussian_noise_sitk(image: sitk.Image,
                        mean: Union[int, float],
                        sigma: Union[int, float],
                        seed: int = None,
                        *args, **kwargs) -> sitk.Image:

    image_default_pixel_type = image.GetPixelID()

    gaussian_noise_filter = sitk.AdditiveGaussianNoiseImageFilter()
    gaussian_noise_filter.SetMean(mean)
    gaussian_noise_filter.SetStandardDeviation(sigma)

    if seed is not None:
        gaussian_noise_filter.SetSeed(seed)

    rescast_filter = sitk.CastImageFilter()
    rescast_filter.SetOutputPixelType(sitk.sitkFloat64)
    image = rescast_filter.Execute(image)

    output_image = gaussian_noise_filter.Execute(image)

    if image_default_pixel_type != sitk.sitkFloat64:
        output_image = sitk.Cast(output_image, image_default_pixel_type)

    return output_image


def change_image_gamma_sitk(image: sitk.Image,
                            gamma: Union[int, float],
                            *args, **kwargs) -> sitk.Image:

    exp_image_filter = sitk.PowImageFilter()
    output_image = exp_image_filter.Execute(image, gamma)

    return output_image