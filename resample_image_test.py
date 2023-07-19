# from Transformations.Spatial.elastic_deformation import random_elastic_deformation_transform
from ImageUtils.ResampleImage import resample_image
import SimpleITK as sitk
import numpy as np



if __name__ == '__main__':


    img = sitk.ReadImage('010_initial.nii.gz')


    grid_nodes = 7
    deformation_value = 50

    rand_gen = np.random.default_rng(0)

    coord = (262, 192, 142)
    t, t_inv = random_elastic_deformation_transform(image_size=img.GetSize(), image_spacing=img.GetSpacing(),
                                                    image_direction=img.GetDirection(),
                                                    image_origin=img.GetOrigin(),
                                                    num_grid_points=grid_nodes,
                                                    max_deformation_displacement=deformation_value,
                                                    use_old_deformation=False,
                                                    seed=rand_gen,
                                                    )


    img_resampled = resample_image(img, interpolator=sitk.sitkLinear, transform=t,)



    sitk.WriteImage(img_resampled, '010_transformed.nii.gz')


    img_inv = resample_image(img_resampled, interpolator=sitk.sitkLinear, transform=t_inv,)

    sitk.WriteImage(img_inv, '010_transformed_inv.nii.gz')


    phys_original = img.TransformIndexToPhysicalPoint(coord)

    transformed_coord = t_inv.TransformPoint(phys_original)
    new_index_coord = img_resampled.TransformPhysicalPointToIndex(transformed_coord)


    a = 1






