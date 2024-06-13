from typing import Union, Tuple, List
import SimpleITK as sitk
import numpy as np

class TransformCoordinate:

    def __init__(self,
                 *args, **kwargs):

        pass


    def transform_coordinate(self,
                             phys_coordinate: Union[List[Union[float, int]], Tuple[Union[float, int], ...], float],
                             transform: sitk.Transform,
                             *args, **kwargs) -> Union[List[Union[float, int]], Tuple[Union[float, int], ...], float]:

        transform_coord = transform.TransformPoint(phys_coordinate)

        return transform_coord
