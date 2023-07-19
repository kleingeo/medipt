from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np

# from .spatial_transform import SpatialTransform
# from .random_affine_transform import RandomAffineTransform



class TransformCoordinate:

    def __init__(self,
                 *args, **kwargs):

        pass


    def transform_coordinate(self,
                             phys_coordinate: Union[List[float, int], Tuple[Union[float, int], ...], float,],
                             transform: sitk.Transform,
                             *args, **kwargs):


        transform_coord = transform.TransformPoint(phys_coordinate)

        return transform_coord
