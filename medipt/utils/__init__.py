from .random_float import random_uniform_float, random_binomial
from .spatial_utils import *
import SimpleITK as sitk


def set_num_workers(n_threads):
    sitk.ProcessObject.SetGlobalDefaultNumberOfThreads(n_threads)