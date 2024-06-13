import SimpleITK as sitk
from typing import Union

def threshold_crop_background(image: sitk.Image,
                              inside_value: Union[int, float],
                              outside_value: Union[int, float],
                              *args, **kwargs) -> sitk.Image:


    binary_image_filter = sitk.OtsuThresholdImageFilter()
    binary_image_filter.SetInsideValue(inside_value)
    binary_image_filter.SetOutsideValue(outside_value)

    binary_image = binary_image_filter.Execute(image)

    label_shape_filter = sitk.LabelShapeStatisticsImageFilter()
    label_shape_filter.Execute(binary_image)
    bounding_box = label_shape_filter.GetBoundingBox(outside_value)
    # The bounding box's first "dim" entries are the starting index and last "dim" entries the size

    cropped_image = sitk.RegionOfInterest(image, bounding_box[int(len(bounding_box)/2):], bounding_box[0:int(len(bounding_box)/2)])

    return cropped_image