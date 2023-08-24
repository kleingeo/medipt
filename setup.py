
from setuptools import (
    Command,
    Extension,
    setup,
    find_packages,
)
from setuptools.command.build_ext import build_ext as _build_ext
import versioneer



setup(
    name='medipt',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(include=['medipt', 'medipt.*']),
    # package_dir={'': 'medipt'},
    install_requires=['requirements.txt'],
    url='https://github.com/kleingeo/ImageProcessingTools',
    license='BSD 3-Clause',
    author='Geoff Klein',
    description='Medical Imaging Processing Tools'
)