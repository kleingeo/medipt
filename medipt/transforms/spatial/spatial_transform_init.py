from abc import ABC, abstractmethod
import numpy as np
import SimpleITK as sitk
from typing import Union, Tuple, List
from types import ModuleType
from ...utils.random_float import initialize_rand_state

from .composite_transform import CompositeTransform
from .rotation_transform import RotationTransform, RandomRotation
from .scaling_transform import ScalingTransform, RandomScaling, RandomUniformScaling
from .flipping_transform import FlippingTransform, RandomFlipping

from .elastic_deformation_transform import (
    ElasticDeformation,
    RandomElasticDeformation,
    ElasticDeformationInputImage,
    RandomElasticDeformationTransformInputImage,
    RandomElasticDeformationTransformOutputImage)

from .translation_transform import (
    TranslationTransform,
    RandomTranslation,
    RandomCoordTranslation,
    RandomBBoxTranslation,
    TranslateInputCenterToOutputCenter,
    TranslateInputOriginToOutputCenter,
    TranslateInputCenterToInputOrigin,
    TranslateRandomInputCenterToInputOrigin)

    # TranslateInputOriginToInputCenter, TranslateInputOriginToOutputOrigin, \
    # TranslateInputCenterToOutputOrigin, \




class SpatialTransformInit:
    def __init__(self,
                 dim: int = 3,
                 used_dimensions: bool = None,
                 seed: Union[np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                 legacy_random_state: bool = True,
                 rand_init: Union[ModuleType, np.random.Generator, np.random.BitGenerator] = None,
                 *args, **kwargs
                 ):

        self.used_dimensions = used_dimensions or [True] * dim
        self.dim = dim
        self.seed = seed
        self.legacy_random_state = legacy_random_state

        if rand_init is None:
            self.rand_init = initialize_rand_state(self.seed, self.legacy_random_state)
        else:
            self.rand_init = rand_init

    # Rotation Transforms

    def rotation_transform(self,
                           *args, **kwargs):
        return RotationTransform(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_rotation_transform(self,
                                  *args, **kwargs):

        return RandomRotation(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    # Scaling Transforms

    def scaling_transform(self,
                            *args, **kwargs):
        return ScalingTransform(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_scaling_transform(self,
                                 *args, **kwargs):
        return RandomScaling(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_uniform_scaling_transform(self,
                                         *args, **kwargs):
        return RandomUniformScaling(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    # Flipping Transforms

    def flipping_transform(self,
                           *args, **kwargs):
        return FlippingTransform(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_flipping_transform(self,
                                  *args, **kwargs):
        return RandomFlipping(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)





    # Translation Transforms

    def translation_transform(self,
                              *args, **kwargs):
        return TranslationTransform(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_translation_transform(self,
                                     *args, **kwargs):
        return RandomTranslation(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    def random_coord_translation(self,
                                 *args, **kwargs):
        return RandomCoordTranslation(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    def random_bbox_translation(self,
                                *args, **kwargs):
        return RandomBBoxTranslation(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    def translate_input_center_to_input_origin(self,
                                               *args, **kwargs):
        return TranslateInputCenterToInputOrigin(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    def translate_random_input_center_to_input_origin(self,
                                               *args, **kwargs):
        return TranslateRandomInputCenterToInputOrigin(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    def translate_input_origin_to_output_center(self,
                                                *args, **kwargs):
        return TranslateInputOriginToOutputCenter(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)



    def translate_input_center_to_output_center(self,
                                                *args, **kwargs):
        return TranslateInputCenterToOutputCenter(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)


    # def translate_input_origin_to_input_center(self,
    #                                            *args, **kwargs):
    #     return TranslateInputOriginToInputCenter(
    #         dim=self.dim,
    #         used_dimensions=self.used_dimensions,
    #         seed=self.seed,
    #         legacy_random_state=self.legacy_random_state,
    #         *args, **kwargs)
    #
    # def translate_input_origin_to_output_origin(self,
    #                                             *args, **kwargs):
    #     return TranslateInputOriginToOutputOrigin(
    #         dim=self.dim,
    #         used_dimensions=self.used_dimensions,
    #         seed=self.seed,
    #         legacy_random_state=self.legacy_random_state,
    #         *args, **kwargs)
    #
    # def translate_input_center_to_output_origin(self,
    #                                             *args, **kwargs):
    #     return TranslateInputCenterToOutputOrigin(
    #         dim=self.dim,
    #         used_dimensions=self.used_dimensions,
    #         seed=self.seed,
    #         legacy_random_state=self.legacy_random_state,
    #         *args, **kwargs)
    #
    #
    # def transate_input_origin_to_output_center(self,
    #                                            *args, **kwargs):
    #     return TranslateInputOriginToOutputCenter(
    #         dim=self.dim,
    #         used_dimensions=self.used_dimensions,
    #         seed=self.seed,
    #         legacy_random_state=self.legacy_random_state,
    #         *args, **kwargs)



    # Elastic Deformation Transforms

    def elastic_deformation_transform(self,
                                      *args, **kwargs):
        return ElasticDeformation(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_elastic_deformation_transform(self,
                                             *args, **kwargs):
        return RandomElasticDeformation(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def elastic_deformation_input_image(self,
                                        *args, **kwargs):
        return ElasticDeformationInputImage(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_elastic_deformation_input_image(self,
                                               *args, **kwargs):
        return RandomElasticDeformationTransformInputImage(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)

    def random_elastic_deformation_output_image(self,
                                                *args, **kwargs):
        return RandomElasticDeformationTransformOutputImage(
            dim=self.dim,
            used_dimensions=self.used_dimensions,
            seed=self.seed,
            legacy_random_state=self.legacy_random_state,
            rand_init=self.rand_init,
            *args, **kwargs)