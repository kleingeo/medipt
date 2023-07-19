from typing import Union, Tuple, List
from ImageProcessingTools.utils import random_uniform_float
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform


class ElasticDeformationTransform(SpatialTransform):
    """
    Rotation transformation base class.
    """

    def __init__(self,
                 dim: int = 3,
                 used_dimensions: bool = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):
        """
        Initializer
        :param dim: The dimension.
        :param used_dimensions: Boolean list of which dimension indizes to use for the transformation.
        :param args: Arguments passed to super init.
        :param kwargs: Keyword arguments passed to super init.
        """


        super(ElasticDeformationTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)

        self.spline_params = None
        self.transform = None
        self.inverse_transform = None
        self.transform_created = False

        self.spline_order = None
        self.num_grid_points = None

        self.image_size = None
        self.image_spacing = None
        self.image_origin = None
        self.image_direction = None



    def _get_deform_transform(self,
                              spline_params: List[float],
                              *args, **kwargs):


        direction_reshape = np.reshape(self.image_direction, (self.dim, self.dim))
        physical_dimensions = np.matmul(direction_reshape * self.image_spacing, self.image_size)

        mesh_size = [grid_node - self.spline_order for grid_node in self.num_grid_points]
        t = sitk.BSplineTransform(self.dim, self.spline_order)
        t.SetTransformDomainOrigin(self.image_origin)
        t.SetTransformDomainMeshSize(mesh_size)
        t.SetTransformDomainPhysicalDimensions(physical_dimensions)
        t.SetTransformDomainDirection(self.image_direction)

        t.SetParameters(spline_params)

        return t

    def get_transform(
            self,
            spline_params: Union[List[float], np.ndarray],
            image_size: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
            image_spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
            image_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
            image_direction: Union[List[Union[int, float]], Tuple[Union[int, float]]] = None,

            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
            # max_deformation_displacement: Union[List[Union[int, float]], Tuple[Union[int, float], ...], np.ndarray] = 50,
            spline_order: int = 3,

            *args, **kwargs):

        self.spline_params = spline_params

        self.spline_order = spline_order

        if isinstance(num_grid_points, (int, float)):
            num_grid_points = tuple([int(num_grid_points)] * self.dim)

        else:
            assert len(num_grid_points) == self.dim, 'Make sure dimensions align for num_grid_points'

        self.num_grid_points = num_grid_points


        image_params = self.get_image_params(image_size=image_size,
                                             image_spacing=image_spacing,
                                             image_origin=image_origin,
                                             image_direction=image_direction,
                                             *args, **kwargs)

        self.image_size = image_params[0]
        self.image_spacing = image_params[1]
        self.image_origin = image_params[2]
        self.image_direction = image_params[3]


        if isinstance(spline_params, np.ndarray):
            spline_params = spline_params.flatten(order='F').tolist()

        self.transform = self._get_deform_transform(spline_params, *args, **kwargs)

        # self.t = t
        #
        # return self.t



    # def get_transform_on_input(
    #         self,
    #         spline_params: Union[List[float], np.ndarray],
    #         num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
    #         spline_order: int = 3,
    #         *args, **kwargs):
    #
    #
    #     self.get_image_params(*args, **kwargs)
    #
    #
    #     t = self.get_transform(spline_params=spline_params,
    #                            num_grid_points=num_grid_points,
    #                            spline_order=spline_order,
    #                            image_size=self.input_size,
    #                            image_spacing=self.input_spacing,
    #                            image_origin=self.input_origin,
    #                            image_direction=self.input_direction,
    #                            *args, **kwargs)
    #
    #     return t
    #
    # def get_transform_on_output(
    #         self,
    #         spline_params: Union[List[float], np.ndarray],
    #         num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
    #         spline_order: int = 3,
    #         *args, **kwargs):
    #
    #     self.get_image_params(*args, **kwargs)
    #
    #     t = self.get_transform(spline_params=spline_params,
    #                            num_grid_points=num_grid_points,
    #                            spline_order=spline_order,
    #                            image_size=self.output_size,
    #                            image_spacing=self.output_spacing,
    #                            image_origin=self.output_size,
    #                            image_direction=self.output_direction,
    #                            *args, **kwargs)
    #
    #     return t

    def get_inverse_transform(self, *args, **kwargs):

        if self.transform is not None:
            if isinstance(self.spline_params, np.ndarray):
                spline_params_inv = -1 * self.spline_params
            else:
                spline_params_inv = [-1 * param for param in self.spline_params]


            self.inverse_transform = self._get_deform_transform(spline_params_inv, *args, **kwargs)

            # self.t_inv = t_inv

        else:
            raise ValueError('No transform found. Call get_transform first.')




class ElasticDeformationTransformInputImage(ElasticDeformationTransform):

    def get_transform_on_input(
            self,
            spline_params: Union[List[float], np.ndarray],
            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
            spline_order: int = 3,
            *args, **kwargs):


        self.get_image_params(*args, **kwargs)


        self.get_transform(spline_params=spline_params,
                               num_grid_points=num_grid_points,
                               spline_order=spline_order,
                               image_size=self.input_size,
                               image_spacing=self.input_spacing,
                               image_origin=self.input_origin,
                               image_direction=self.input_direction,
                               *args, **kwargs)

        # return t


class ElasticDeformationTransformOutputImage(ElasticDeformationTransform):

    def get_transform_on_output(
            self,
            spline_params: Union[List[float], np.ndarray],
            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
            spline_order: int = 3,
            *args, **kwargs):

        self.get_image_params(*args, **kwargs)

        self.get_transform(spline_params=spline_params,
                           num_grid_points=num_grid_points,
                           spline_order=spline_order,
                           image_size=self.output_size,
                           image_spacing=self.output_spacing,
                           image_origin=self.output_size,
                           image_direction=self.output_direction,
                           *args, **kwargs)

        # return t


class RandomElasticDeformationTransform(ElasticDeformationTransform):

    def __init__(self,
                 dim: int = 3,
                 used_dimensions: bool = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):


        super(RandomElasticDeformationTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)



    def get_random_spline_params(
            self,
            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], np.ndarray] = 7,
            max_deformation_displacement: Union[List[Union[int, float]], Tuple[Union[int, float], ...], np.ndarray] = 50,
            *args, **kwargs, ) -> np.ndarray:

        output_size = *num_grid_points, self.dim

        spline_params = random_uniform_float(-1, 1, output_size,
                                             seed=self.seed, legacy_random_state=self.legacy_random_state)

        for dimension in range(self.dim):
            spline_params[..., dimension] *= max_deformation_displacement[dimension]

        return spline_params


    def get_random_transform(
            self,
            image_size: Union[int, float, List[Union[int, float]], Tuple[Union[int, float], ...], np.ndarray],
            image_spacing: Union[int, float, List[Union[int, float]], Tuple[Union[int, float], ...], np.ndarray],
            image_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...], np.ndarray] = None,
            image_direction: Union[List[Union[int, float]], Tuple[Union[int, float]], np.ndarray] = None,


            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
            max_deformation_displacement: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 50,


            spline_order: int = 3,

            *args, **kwargs):


        self.spline_params = self.get_random_spline_params(num_grid_points, max_deformation_displacement,
                                                           *args, **kwargs)


        self.get_transform(self.spline_params,
                           image_size=image_size, image_spacing=image_spacing,
                           image_origin=image_origin, image_direction=image_direction,
                           num_grid_points=num_grid_points,
                           max_deformation_displacement=max_deformation_displacement,
                           spline_order=spline_order,
                           *args, **kwargs)


        # return self.t



class RandomElasticDeformationTransformInputImage(RandomElasticDeformationTransform):
    def get_random_transform_on_input(
            self,
            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
            max_deformation_displacement: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 50,
            spline_order: int = 3,
            *args, **kwargs):

        self.get_image_params(*args, **kwargs)

        self.get_random_transform(num_grid_points=num_grid_points,
                                  max_deformation_displacement=max_deformation_displacement,
                                  spline_order=spline_order,
                                  image_size=self.input_size,
                                  image_spacing=self.input_spacing,
                                  image_origin=self.input_origin,
                                  image_direction=self.input_direction,
                                  *args, **kwargs)

        # return t


class RandomElasticDeformationTransformOutputImage(RandomElasticDeformationTransform):
    def get_random_transform_on_output(
            self,
            num_grid_points: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 7,
            max_deformation_displacement: Union[List[Union[int, float]], Tuple[Union[int, float], ...], int, float] = 50,
            spline_order: int = 3,
            *args, **kwargs):

        self.get_image_params(*args, **kwargs)

        self.get_random_transform(num_grid_points=num_grid_points,
                                  max_deformation_displacement=max_deformation_displacement,
                                  spline_order=spline_order,
                                  image_size=self.output_size,
                                  image_spacing=self.output_spacing,
                                  image_origin=self.output_size,
                                  image_direction=self.output_direction,
                                  *args, **kwargs)

        # return t