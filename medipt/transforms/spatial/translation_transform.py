from typing import Union, Tuple, List
from ...utils import random_uniform_float
from ...utils import physical_image_size_no_origin, physical_image_size
import SimpleITK as sitk
import numpy as np

from .spatial_transform import SpatialTransform
from .random_affine_transform import RandomAffineTransform




class TranslationTransform(SpatialTransform):
    """
    Translation transformation base class.
    """
    # def __init__(self,
    #              dim: int = 3,
    #              used_dimensions: bool = None,
    #              seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
    #              legacy_random_state: bool = True,
    #              *args, **kwargs):
    #     """
    #     Initializer
    #     :param dim: The dimension.
    #     :param used_dimensions: Boolean list of which dimension indizes to use for the transformation.
    #     :param args: Arguments passed to super init.
    #     :param kwargs: Keyword arguments passed to super init.
    #     """
    #
    #     super(TranslationTransform, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)
    #
    #     assert len(self.used_dimensions) == dim, 'Length of used_dimensions must be equal to dim.'

    def _get_transform(self,
                      translation: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs):
        """
        Returns the sitk transform based on the given parameters.
        :param dim: The dimension.
        :param offset: List of offsets for each dimension.
        :return: The sitk.AffineTransform().
        """

        assert len(translation) == self.dim, 'Length of offset must be equal to dim.'

        t = sitk.AffineTransform(self.dim)
        t.Translate(translation)

        self.transform = t
        # return t

    def get_transform(self,
                      translation: Union[List[float], Tuple[float, ...], float],
                      *args, **kwargs):

        self._get_transform(translation, *args, **kwargs)


class RandomTranslation(RandomAffineTransform, TranslationTransform):
    """
    A translation transformation with a random offset.
    """
    # def __init__(self,
    #              # min_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
    #              # max_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
    #              dim: Union[int, None] = 3,
    #              used_dimensions: bool = None,
    #
    #              seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
    #              legacy_random_state: bool = True,
    #              *args, **kwargs):
    #     """
    #     Initializer.
    #     :param dim: The dimension.
    #     :param random_offset: List of random offsets per dimension. Random offset is calculated uniformly within [-random_offset[i], random_offset[i]]
    #     :param args: Arguments passed to super init.
    #     :param kwargs: Keyword arguments passed to super init.
    #     """
    #
    #     super(RandomTranslation, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)

    def get_random_transform(self,
                             min_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
                             max_trans: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
                             transformation_dict=None,
                             *args, **kwargs):


        self._get_random_transform(min_trans, max_trans, *args, **kwargs)
        # return self.transform


class RandomCoordTranslation(RandomAffineTransform, TranslationTransform):
    def __init__(self,
                 dim: Union[int, None] = 3,
                 used_dimensions: bool = None,

                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 *args, **kwargs):
        """
        Initializer.
        :param dim: The dimension.
        :param random_offset: List of random offsets per dimension. Random offset is calculated uniformly within [-random_offset[i], random_offset[i]]
        :param args: Arguments passed to super init.
        :param kwargs: Keyword arguments passed to super init.
        """

        super(RandomCoordTranslation, self).__init__(dim, used_dimensions, seed, legacy_random_state, *args, **kwargs)


    def get_random_transform(self,
                             coord: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
                             translation_extent: Union[Union[List[Union[int, float]], Tuple[Union[int, float], ...]], int, float, np.integer, np.floating, np.ndarray],
                             transformation_dict: dict = None,
                             *args, **kwargs):



        if isinstance(translation_extent, (int, float, np.floating, np.integer)):
            translation_extent = np.ndarray([translation_extent] * self.dim)
        elif isinstance(translation_extent, (tuple, list)):
            translation_extent = np.array(translation_extent)
        elif isinstance(translation_extent, np.ndarray):
            if len(translation_extent) < self.dim:
                translation_extent = np.array([translation_extent] * self.dim)


        if isinstance(coord, (int, float, np.floating, np.integer)):
            coord = np.ndarray([coord] * self.dim)
        elif isinstance(coord, (tuple, list)):
            coord = np.array(coord)

        assert len(coord) == len(translation_extent), "coord and translation_extent must have the same length."


        coord_min = coord - translation_extent
        coord_max = coord + translation_extent

        self._get_random_transform(min_range=coord_min, max_range=coord_max, transformation_dict=transformation_dict,
                                   offset=coord, *args, **kwargs)


class TranslateInputCenterToInputOrigin(TranslationTransform):
    def get_transform(self,
                      *args, **kwargs):

        input_center_phys = self.get_input_center(*args, **kwargs)
        input_origin_phys = self.get_input_origin(*args, **kwargs)

        # translation = tuple([input_center_phys[i] - input_origin_phys[i] for i in range(self.dim)])
        translation = tuple([input_center_phys[i] for i in range(self.dim)])

        self._get_transform(translation)

        # return self.t



class TranslateRandomInputCenterToInputOrigin(TranslationTransform):
    def get_transform(self,
                      *args, **kwargs):

        input_center_phys = self.get_random_point(*args, **kwargs)
        input_origin_phys = self.get_input_origin(*args, **kwargs)

        # translation = tuple([input_center_phys[i] - input_origin_phys[i] for i in range(self.dim)])
        translation = tuple([input_center_phys[i] for i in range(self.dim)])

        self._get_transform(translation)

        # return self.t



class TranslateInputOriginToOutputCenter(TranslationTransform):
    def get_transform(self,
                      *args, **kwargs):

        input_origin_phys = self.get_input_origin(*args, **kwargs)
        output_center_phys = self.get_output_center(*args, **kwargs)

        # translation = tuple([input_origin_phys[i] - output_center_phys[i] for i in range(self.dim)])
        translation = tuple([-output_center_phys[i] for i in range(self.dim)])

        self._get_transform(translation)


class TranslateInputCenterToOutputCenter(TranslationTransform):
    def get_transform(self,
                      *args, **kwargs):

        input_center_phys = self.get_input_center(*args, **kwargs)
        output_center_phys = self.get_output_center(*args, **kwargs)


        translation = tuple([input_center_phys[i] - output_center_phys[i] for i in range(self.dim)])

        self._get_transform(translation)

        # return self.t


class TranslateInputCenterToOutputCenter(TranslationTransform):
    def get_transform(self,
                      *args, **kwargs):

        input_center_phys = self.get_input_center(*args, **kwargs)
        output_center_phys = self.get_output_center(*args, **kwargs)


        translation = tuple([input_center_phys[i] - output_center_phys[i] for i in range(self.dim)])

        self._get_transform(translation)

        # return self.t



#
# class TranslateInputOriginToInputCenter(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_origin_phys = self.get_input_origin(*args, **kwargs)
#         input_center_phys = self.get_input_center(*args, **kwargs)
#
#         translation = tuple([input_origin_phys[i] - input_center_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t
#
#
#
# class TranslateInputOriginToOutputOrigin(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_origin_phys = self.get_input_origin(*args, **kwargs)
#         output_origin_phys = self.get_output_origin(*args, **kwargs)
#
#
#         translation = tuple([input_origin_phys[i] - output_origin_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t
#
#
#
#
#
#
#
# class TranslateInputCenterToOutputOrigin(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_center_phys = self.get_input_center(*args, **kwargs)
#         output_origin_phys = self.get_input_origin(*args, **kwargs)
#
#
#         translation = tuple([input_center_phys[i] - output_origin_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)






















# class TranslateInputCenterToInputOrigin(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_origin_phys = self.get_input_origin(*args, **kwargs)
#         input_center_phys = self.get_input_center(*args, **kwargs)
#
#
#         translation = tuple([input_center_phys[i] - input_origin_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t
#
#
#
# class TranslateInputOriginToOutputCenter(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         output_center_phys = self.get_output_center(*args, **kwargs)
#         input_origin_phys = self.get_input_origin(*args, **kwargs)
#
#
#         translation = tuple([input_origin_phys[i] - output_center_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
# class TranslateOutputOriginToOutputCenter(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         output_center_phys = self.get_output_center(*args, **kwargs)
#         output_origin_phys = self.get_output_origin(*args, **kwargs)
#
#         translation = tuple([output_origin_phys[i] - output_center_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t
#
# class TranslateInputCenterToOutputOrigin(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_center_phys = self.get_input_center(*args, **kwargs)
#         # output_origin_phys = self.get_output_origin(*args, **kwargs)
#         output_center_phys = self.get_output_center(*args, **kwargs)
#
#         translation = tuple([-input_center_phys[i] + output_center_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t
#
# class TranslateInputOriginToOutputOrigin(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_origin_phys = self.get_input_origin(*args, **kwargs)
#         # output_origin_phys = self.get_output_origin(*args, **kwargs)
#         output_center_phys = self.get_output_center(*args, **kwargs)
#
#         translation = tuple([input_origin_phys[i] - output_center_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t
#
#
#
# class TranslateOutputCenterToOutputOrigin(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         output_center_phys = self.get_output_center(*args, **kwargs)
#         output_origin_phys = self.get_output_origin(*args, **kwargs)
#
#         translation = tuple([output_center_phys[i] - output_origin_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
# class TranslateInputCenterToOutputCenter(TranslationTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_center_phys = self.get_input_center(*args, **kwargs)
#         output_center_phys = self.get_output_center(*args, **kwargs)
#
#         translation = tuple([input_center_phys[i] - output_center_phys[i] for i in range(self.dim)])
#
#         self._get_transform(translation)
#
#         # return self.t




# class TranslateInputCenterToOutputCenter(TranslateTransform):
#     def get_transform(self,
#                       *args, **kwargs):
#
#         input_center_phys = self.get_input_center(*args, **kwargs)
#         output_center_phys = self.get_output_center(*args, **kwargs)
#
#         # additional = [70, 70, 0]
#         additional = [0, 0, 0]
#         translation = tuple([input_center_phys[i] - output_center_phys[i] + additional[i] for i in range(self.dim)])
#
#
#
#
#         # translation = self.get_output_center(*args, **kwargs) self.get_input_origin(*args, **kwargs)
#         #
#         # translation = [-1 * t for t in translation]
#
#         self._get_transform(translation)


class RandomBBoxTranslation(RandomAffineTransform, TranslationTransform):
    def get_random_transform(self,
                             transformation_dict: dict = None,
                             *args, **kwargs):

        bbox_center_start = kwargs.get('centroids_bb_start', None)
        bbox_center_end = kwargs.get('centroids_bb_end', None)



        if (bbox_center_start is None) and (bbox_center_end is None):
            raise ValueError('Centroid bounding box start and end must be provided when using '
                             '"RandomBBoxTranslation".')

        bbox_extent = bbox_center_end - bbox_center_start

        output_size = kwargs.get('output_size', None)
        output_spacing = kwargs.get('output_spacing', None)
        output_direction = kwargs.get('output_direction', None)
        dim = kwargs.get('dim', None)

        output_image_size_phys = physical_image_size_no_origin(dim=dim,
                                                               size=output_size,
                                                               spacing=output_spacing,
                                                               direction=output_direction)

        try:
            extra_space = bbox_extent - np.array(output_image_size_phys)
        except:
            a = 1

        # Only translate if the bbox is larger than the output image size
        extra_space[extra_space < 0] = 0

        max_trans = extra_space / 2
        min_trans = extra_space / 2 * -1


        self._get_random_transform(min_trans, max_trans, transformation_dict=transformation_dict,
                                   *args, **kwargs)











class RandomFactorInput(TranslationTransform):
    """
    A translation transform that translates the input image by a random factor, such that it will be cropped.
    The input center should usually be at the origin before this transformation.
    The actual translation value per dimension will be calculated as follows:
    (input_size[i] * input_spacing[i] - self.remove_border[i]) * float_uniform(-self.random_factor[i], self.random_factor[i]) for each dimension.
    """
    def get_transform(self,
                      random_factor,
                      remove_border=None,
                      *args, **kwargs):
        """
        Returns the sitk transform based on the given parameters.
        :param kwargs: Must contain either 'image', or 'input_size' and 'input_spacing', which define the input image physical space.
        :return: The sitk.AffineTransform().
        """

        # TODO check to see if this works for arbitrary input directions and origins


        remove_border = remove_border or [0.0] * self.dim

        self.get_input_output_space(*args, **kwargs)

        # assert np.allclose(self.input_direction, np.eye(self.dim).flatten()), 'this transformation only works for eye direction, is: ' + self.input_direction
        # assert np.allclose(self.input_origin, np.zeros(self.dim)), 'this transformation only works for zeros origin, is: ' + self.input_origin


        phys_input_size = physical_image_size_no_origin(dim=self.dim,
                                                        size=self.input_size,
                                                        spacing=self.input_spacing,
                                                        direction=self.input_direction)

        phys_input_size = np.array(phys_input_size) - np.array(remove_border)

        random_factor = np.array(random_factor)

        random_scaling = np.array(random_uniform_float(low_value=-random_factor, high_value=random_factor,
                                                       output_size=self.dim,
                                                       seed=self.seed, legacy_random_state=self.legacy_random_state))

        translation = list(phys_input_size * random_scaling)

        self.transform = self._get_transform(translation)

