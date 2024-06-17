import SimpleITK as sitk
import numpy as np
from typing import Union, Tuple, List
from .spatial_transform import SpatialTransform
from .elastic_deformation_transform import ElasticDeformation

def composite_transform(transforms: List[Union[sitk.AffineTransform, sitk.BSplineTransform, sitk.DisplacementFieldTransform]],
                        dim: int = 3):

    if sitk.Version_MajorVersion() == 1:
        compos = sitk.Transform(dim, sitk.sitkIdentity)
        for transformation in transforms:
            compos.AddTransform(transformation)
    else:
        compos = sitk.CompositeTransform(transforms)


    return compos



class CompositeTransform:
    def __init__(self,
                 *args, **kwargs):

        self.transforms = []


    def add_transforms(self,
                       transform: Union[List[Union[SpatialTransform, sitk.Transform]],
                                        Tuple[Union[SpatialTransform, sitk.Transform], ...],
                                        Union[SpatialTransform, sitk.Transform]]):

        if isinstance(transform, (tuple, list)):
            self.transforms.extend(transform)

        else:
            self.transforms.append(transform)

    def create_composite(self, dim: int = 3) -> sitk.Transform:
        compos = sitk.CompositeTransform(dim)
        for transform in self.transforms:
            if isinstance(transform, SpatialTransform):
                sitk_transform = transform.transform
                compos.AddTransform(sitk_transform)
            else:
                compos.AddTransform(transform.transform)

        return compos

    def create_inverse_composite(self, dim: int = 3,
                                 use_displacement_field: bool = False) -> sitk.CompositeTransform:
        compos = sitk.CompositeTransform(dim)

        for transform in self.transforms[::-1]:
            if isinstance(transform, SpatialTransform):

                if isinstance(transform, ElasticDeformation):
                    if use_displacement_field:
                        transform.get_inverted_transform_from_displacement()
                        sitk_inverse_transform = transform.inverted_transform_from_displacement

                    else:
                        transform.get_inverse_transform()
                        sitk_inverse_transform = transform.inverse_transform

                else:
                    transform.get_inverse_transform()
                    sitk_inverse_transform = transform.inverse_transform

                # if use_displacement_field:
                #     transform.get_inverted_transform_from_displacement()
                #     sitk_inverse_transform = transform.inverted_transform_from_displacement
                #
                # else:
                #     transform.get_inverse_transform()
                #     sitk_inverse_transform = transform.inverse_transform


                compos.AddTransform(sitk_inverse_transform)

            else:
                if use_displacement_field:
                    raise Warning("The use_displacement_field option is not implemented for SimpleITK transforms.")
                compos.AddTransform(transform.GetInverse())

        return compos


