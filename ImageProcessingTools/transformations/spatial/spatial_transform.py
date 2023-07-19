from abc import ABC, abstractmethod
import numpy as np
import SimpleITK as sitk
from typing import Union, Tuple, List
from ImageProcessingTools.transformations import image_index_to_phys
from ImageProcessingTools.utils.image_input_output_space import resolve_input_output_space

class SpatialTransform(ABC):
    """
    A generic spatial transform that can be applied to 2D and 3D images.
    """
    def __init__(self,
                 dim: int = 3,
                 used_dimensions: bool = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):
        """
        Initializer.
        :param dim: The dimension of the transformation.
        :param args: Arguments passed to super init.
        :param kwargs: Keyword arguments passed to super init.
        """


        self.used_dimensions = used_dimensions or [True] * dim
        self.dim = dim

        self.seed = seed
        self.legacy_random_state = legacy_random_state

        self.transform = None

        self.inverse_transform = None

        assert len(self.used_dimensions) == dim, 'Length of used_dimensions must be equal to dim.'


        self.input_size = None
        self.input_space = None
        self.input_origin = None
        self.input_direction = None

        self.image_params_gathered = False


        self.output_size = None
        self.output_spacing = None
        self.output_origin = None
        self.output_direction = None


    @abstractmethod
    def _get_transform(self,
                      transform_params: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs):

        raise NotImplementedError('This method must be implemented in a child class.')



    def get_image_params(
            self,
            image: sitk.Image = None,
            image_size: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
            image_spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
            image_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
            image_direction: Union[List[Union[int, float]], Tuple[Union[int, float]]] = None,
            *args, **kwargs):


        if image is not None:
            image_size = image.GetSize()
            image_spacing = image.GetSpacing()
            image_origin = image.GetOrigin()
            image_direction = image.GetDirection()

        else:
            image_size = kwargs.get('image_size', image_size)
            image_spacing = kwargs.get('image_spacing', image_spacing)
            image_origin = kwargs.get('image_origin', image_origin)
            image_direction = kwargs.get('image_direction', image_direction)



        if image_spacing is None:
            image_spacing = [1.0] * self.dim

        if image_origin is None:
            image_origin = np.zeros(self.dim)

        if image_direction is None:
            image_direction = np.eye(self.dim).flatten(order='F').tolist()


        return image_size, image_spacing, image_origin, image_direction

    def get_input_output_space(self,
                               # input_image: sitk.Image = None,
                               # input_size: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               # output_size: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               # input_spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               #
                               #
                               # output_spacing: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               # input_direction: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               # output_direction: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               # input_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               # output_origin: Union[List[Union[int, float]], Tuple[Union[int, float], ...]] = None,
                               dict: dict = None,
                               *args, **kwargs):

        if dict is None:
            dict = resolve_input_output_space(*args, **kwargs)

        elif len(dict) == 0:
            dict = resolve_input_output_space(*args, **kwargs)


        input_size = dict['input_size']
        input_spacing = dict['input_spacing']
        input_origin = dict['input_origin']
        input_direction = dict['input_direction']

        output_size = dict['output_size']
        output_spacing = dict['output_spacing']
        output_origin = dict['output_origin']
        output_direction = dict['output_direction']


        self.input_size = input_size
        self.input_spacing = input_spacing
        self.input_origin = input_origin
        self.input_direction = input_direction

        self.output_size = output_size
        self.output_spacing = output_spacing
        self.output_origin = output_origin
        self.output_direction = output_direction

        self.image_params_gathered = True


    def get_input_origin(self,
                         *args, **kwargs):

        if self.image_params_gathered is False:
            self.get_input_output_space(*args, **kwargs)

        input_origin_index = (0.0,) * self.dim


        input_origin_phys = image_index_to_phys(dim=self.dim,
                                                index_coords=input_origin_index,
                                                spacing=self.input_spacing,
                                                direction=self.input_direction,
                                                origin=self.input_origin)

        return input_origin_phys

    def get_output_origin(self, *args, **kwargs):

        if self.image_params_gathered is False:
            self.get_input_output_space(*args, **kwargs)

        output_origin_index = (0.0,) * self.dim

        output_origin_phys = image_index_to_phys(dim=self.dim,
                                                 index_coords=output_origin_index,
                                                 spacing=self.output_spacing,
                                                 direction=self.output_direction,
                                                 origin=self.output_origin)

        return output_origin_phys

    def get_input_center(self, *args, **kwargs):
        if self.image_params_gathered is False:
            self.get_input_output_space(*args, **kwargs)


        input_center_index = tuple([(i - 1) / 2 for i in self.input_size])

        input_center_phys = image_index_to_phys(dim=self.dim,
                                                index_coords=input_center_index,
                                                spacing=self.input_spacing,
                                                direction=self.input_direction,
                                                origin=self.input_origin)

        return input_center_phys

    def get_output_center(self, *args, **kwargs):
        if self.image_params_gathered is False:
            self.get_input_output_space(*args, **kwargs)

        output_center_index = tuple([(i - 1) / 2 for i in self.output_size])

        output_center_phys = image_index_to_phys(dim=self.dim,
                                                 index_coords=output_center_index,
                                                 spacing=self.output_spacing,
                                                 direction=self.output_direction,
                                                 origin=self.output_origin)

        return output_center_phys



    def get_inverse_transform(self, *args, **kwargs):


        if self.transform is not None:
            self.inverse_transform = self.transform.GetInverse()

        else:
            raise ValueError('No transform found. Call get_transform first.')

        # return self.inverse_transform
