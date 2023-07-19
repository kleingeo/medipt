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
                             phys_coordinate: Union[List[Union[float, int]], Tuple[Union[float, int], ...], float],
                             transform: sitk.Transform,
                             *args, **kwargs):

#WARNING: autodoc: failed to import module 'composite_transform' from module 'ImageProcessingTools.transformations.spatial'; the following exception was raised:
#cannot import name 'get_output_size_from_spacing' from 'ImageProcessingTools.transformations' (D:\ImageProcessingTools\ImageProcessingTools\transformations\__init__.py)
        transform_coord = transform.TransformPoint(phys_coordinate)

        return transform_coord
