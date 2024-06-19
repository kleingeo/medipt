import SimpleITK as sitk
from medipt.transforms.intensity.scale_gamma_intensity import ScaleGammaIntensity

if __name__ == '__main__':
    image_input = sitk.ReadImage(r'G:\test_images\verse818_image_new.nii.gz')

    scale_gamma_intensity = ScaleGammaIntensity(min_random_gamma=0.9, max_random_gamma=1.1, output_min=0, output_max=1)

    image_output = scale_gamma_intensity(image_input)

    sitk.WriteImage(image_output, r'G:\test_images\verse818_image_new_scaled_gamma.nii.gz')

