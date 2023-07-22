from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np
from ...utils import min_max_intensity, clamp_intensity, shift_scale_intensity, rescale_intensity

# from .spatial_transform import SpatialTransform
# from .random_affine_transform import RandomAffineTransform





def rescale_clamp_intensity(image: sitk.Image,
                            new_min: Union[int, float] = None,
                            new_max: Union[int, float] = None,
                            window_min: Union[int, float] = None,
                            window_max: Union[int, float] = None,
                            shift: Union[int, float] = None,
                            scale: Union[int, float] = None,
                            random_shift: Union[int, float] = None,
                            random_scale: Union[int, float] = None,
                            *args, **kwargs):


    input_image_min_max = min_max_intensity(image)
    output_image = image


    if (window_min is not None) or (window_max is not None):

        output_image = clamp_intensity(output_image,
                                       window_min=window_min,
                                       window_max=window_max,
                                       image_min=input_image_min_max[0],
                                       image_max=input_image_min_max[1],
                                       *args, **kwargs)




    a = sitk.ShiftScale(output_image, shift=-1024, scale=1/2048)


    # sitk.WriteImage(a, 'hold.nii.gz')


    a_image_min_max = min_max_intensity(a)

    b = 1





    if (new_min is not None) or (new_max is not None):

        if new_min is None:
            new_min = window_min if window_min is not None else input_image_min_max[0]

        if new_max is None:
            new_max = window_max if window_max is not None else input_image_min_max[1]


        current_min = window_min if window_min is not None else input_image_min_max[0]
        current_max = window_max if window_max is not None else input_image_min_max[1]

        intens_scaling = (new_max - new_min) / (current_max - current_min)
        shift = new_min - intens_scaling * current_min



        a = 1



    if (shift is None) or (scale is None):




        current_min_max_filter = sitk.MinimumMaximumImageFilter()
        current_min_max_filter.Execute(image)
        current_min = current_min_max_filter.GetMinimum()
        current_max = current_min_max_filter.GetMaximum()


        scale = (new_max - new_min) / (current_max - current_min)

        shift = new_min - scale * current_min


class RescaleClampIntensity:
    def __init__(self,
                 new_min: Union[int, float] = None,
                 new_max: Union[int, float] = None,
                 window_min: Union[int, float] = None,
                 window_max: Union[int, float] = None,
                 shift: Union[int, float] = None,
                 scale: Union[int, float] = None,
                 *args, **kwargs):

        self.new_min = new_min
        self.new_max = new_max

        self.window_min = window_min
        self.window_max = window_max

        self.shift = shift
        self.scale = scale



        # pre-processing: clamp image intensity so minimum is -1024

        # apply transforms

        # post_processing:
            # shift image by minimum and scale by 1/2048
                # this tries to put image between -1 and 1

            # apply random shifts and scales, this is why we put image between -1 and 1

            # clamp image intensity between -1 and 1


    def rescale_intensity(self,
                          image: sitk.Image,
                          *args, **kwargs):


        scaled_image = rescale_clamp_intensity(image,
                                               new_min=self.new_min,
                                               new_max=self.new_max,
                                               window_min=self.window_min,
                                               window_max=self.window_max,
                                               shift=self.shift,
                                               scale=self.scale,
                                               *args, **kwargs)

        return scaled_image



if __name__ == '__main__':


    img = sitk.ReadImage('..\..\..\sub-verse260.nii.gz')


    rescale = RescaleClampIntensity(new_min=-1,
                                    new_max=1,
                                    window_min=-1024)

    rescaled_image = rescale.rescale_intensity(img)
