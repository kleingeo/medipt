import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple, List


def min_max_intensity(image: sitk.Image,
                      *args, **kwargs) -> Tuple[float, float]:

    min_max_filter = sitk.MinimumMaximumImageFilter()
    min_max_filter.Execute(image)

    image_min = min_max_filter.GetMinimum()
    image_max = min_max_filter.GetMaximum()

    return image_min, image_max



def clamp_intensity(image: sitk.Image,
                    window_min: Union[int, float] = None,
                    window_max: Union[int, float] = None,
                    image_min: Union[int, float] = None,
                    image_max: Union[int, float] = None,
                    *args, **kwargs) -> sitk.Image:


    if (window_min is None) and (window_max is None):
        raise ValueError('window_min and window_max cannot both be None.')

    if image_min is None or image_max is None:
        image_min_max = min_max_intensity(image)

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



def shift_scale_intensity(image: sitk.Image,
                          shift: Union[int, float] = None,
                          scale: Union[int, float] = None,
                          *args, **kwargs) -> sitk.Image:

    shift_scale_filter = sitk.ShiftScaleImageFilter()
    shift_scale_filter.SetShift(shift)
    shift_scale_filter.SetScale(scale)
    shifted_scaled_image = shift_scale_filter.Execute(image)

    return shifted_scaled_image


def rescale_intensity(image: sitk.Image,
                      new_min: Union[int, float] = None,
                      new_max: Union[int, float] = None,
                      *args, **kwargs) -> sitk.Image:

    if (new_min is None) or (new_max is None):
        image_min_max = min_max_intensity(image)

        if new_min is None:
            new_min = image_min_max[0]
        if new_max is None:
            new_max = image_min_max[1]

    rescale_filter = sitk.RescaleIntensityImageFilter()
    rescale_filter.SetOutputMinimum(new_min)
    rescale_filter.SetOutputMaximum(new_max)

    rescaled_image = rescale_filter.Execute(image)

    return rescaled_image




def gaussian_blur(image: sitk.Image,
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



def gaussian_noise(image: sitk.Image,
                   mean: Union[int, float],
                   sigma: Union[int, float],
                   *args, **kwargs) -> sitk.Image:

    image_default_pixel_type = image.GetPixelID()

    gaussian_noise_filter = sitk.AdditiveGaussianNoiseImageFilter()
    gaussian_noise_filter.SetMean(mean)
    gaussian_noise_filter.SetStandardDeviation(sigma)

    rescast_filter = sitk.CastImageFilter()
    rescast_filter.SetOutputPixelType(sitk.sitkFloat64)
    image = rescast_filter.Execute(image)

    output_image = gaussian_noise_filter.Execute(image)

    if image_default_pixel_type != sitk.sitkFloat64:
        output_image = sitk.Cast(output_image, image_default_pixel_type)

    return output_image