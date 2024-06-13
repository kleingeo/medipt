
from typing import Dict, Union, List, Tuple
import numpy as np
from medipt.transforms.spatial import SpatialTransformInit
from medipt.transforms.spatial import CompositeTransform

def generate_transform(params: dict,
                       spatial_transform_base: SpatialTransformInit = None,
                       dim: int = 3,
                       seed: Union[
                           np.random.RandomState, np.random.Generator, np.random.BitGenerator, int, None] = None,
                       legacy_random_state: bool = True,
                       *args, **kwargs) -> Tuple[CompositeTransform, list]:

    translate_to_centroid_bbox_center = params.get('translate_to_centroid_bbox_center', False)

    translate_by_random_factor = params.get('translate_by_random_factor', False)

    random_rotation = params.get('random_rotation', False)
    random_translation = params.get('random_translation', False)
    random_scaling = params.get('random_scaling', False)
    random_uniform_scaling = params.get('random_uniform_scaling', False)
    random_flipping = params.get('random_flipping', False)
    random_deformation = params.get('random_elastic_deformation', False)

    transformation_list = []

    if spatial_transform_base is None:
        spatial_transform_base = SpatialTransformInit(dim=dim,
                                                      seed=seed,
                                                      legacy_random_state=legacy_random_state,)

    # Translate from center of bbox to input origin
    if translate_to_centroid_bbox_center:
        translation_to_bbox_center = spatial_transform_base.translation_transform()

        bbox_center_start = params.get('centroids_bb_start', None)
        bbox_center_end = params.get('centroids_bb_end', None)

        if (bbox_center_start is None) or (bbox_center_end is None):
            raise ValueError('Centroid bounding box start and end must be provided when using translate_to_centroid_bbox_center".')

        assert isinstance(bbox_center_start, np.ndarray) and isinstance(bbox_center_end, np.ndarray), 'Centroid bounding box start and end must be a numpy array.'

        extent = bbox_center_end - bbox_center_start

        bbox_center_offset = (extent - 1) / 2 + bbox_center_start


        bbox_center_offset = bbox_center_offset

        translation_to_bbox_center.get_transform(translation=bbox_center_offset)

        transformation_list.append(translation_to_bbox_center)

    else:
        translate_to_img_center = spatial_transform_base.translate_input_center_to_input_origin()

        translate_to_img_center.get_transform(**params)
        transformation_list.append(translate_to_img_center)




    if translate_by_random_factor:
        translation_by_random_factor = spatial_transform_base.random_bbox_translation()

        translation_by_random_factor.get_random_transform(**params)
        transformation_list.append(translation_by_random_factor)

    if random_translation:
        min_translation = -1 * np.array(random_translation)
        max_translation = np.array(random_translation)

        random_translation_transform = spatial_transform_base.random_translation_transform()
        random_translation_transform.get_random_transform(min_trans=min_translation,
                                                          max_trans=max_translation)

        transformation_list.append(random_translation_transform)

    if random_rotation:
        min_angle = -1 * np.array(random_rotation)
        max_angle = np.array(random_rotation)

        random_rotation_transform = spatial_transform_base.random_rotation_transform()
        random_rotation_transform.get_random_transform(min_angles=min_angle, max_angles=max_angle)
        transformation_list.append(random_rotation_transform)

    if random_uniform_scaling:
        min_scaling = -1 * random_uniform_scaling
        max_scaling = random_uniform_scaling

        random_uniform_scaling_transform = spatial_transform_base.random_uniform_scaling_transform()
        random_uniform_scaling_transform.get_random_transform(min_scaling=min_scaling, max_scaling=max_scaling)
        transformation_list.append(random_uniform_scaling_transform)

    if random_scaling:
        min_scaling = -1 * np.array(random_scaling)
        max_scaling = np.array(random_scaling)

        random_scaling_transform = spatial_transform_base.random_scaling_transform()
        random_scaling_transform.get_random_transform(min_scaling=min_scaling, max_scaling=max_scaling)
        transformation_list.append(random_scaling_transform)

    if random_flipping:
        random_flipping_transform = spatial_transform_base.random_flipping_transform()
        random_flipping_transform.get_random_transform(flip_axes=random_flipping)
        transformation_list.append(random_flipping_transform)

    translate_to_output_center = spatial_transform_base.translate_input_origin_to_output_center()
    translate_to_output_center.get_transform(**params)
    transformation_list.append(translate_to_output_center)

    if random_deformation:
        deformation_transform = spatial_transform_base.random_elastic_deformation_transform()
        deformation_transform.get_random_transform(image_size=params['output_size'],
                                                   image_spacing=params['output_spacing'],
                                                   image_origin=params['output_origin'],
                                                   image_direction=params['output_direction'],
                                                   max_deformation_displacement=params['max_deformation'],
                                                   )

        transformation_list.append(deformation_transform)

    composite_transform_obj = CompositeTransform()
    composite_transform_obj.add_transforms(transformation_list)

    return composite_transform_obj, transformation_list
