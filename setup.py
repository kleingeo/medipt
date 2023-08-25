
from setuptools import (
    Command,
    Extension,
    setup,
    find_packages,
)
from setuptools.command.build_ext import build_ext as _build_ext



setup(
    name='medipt',
    packages=find_packages(include=['medipt', 'medipt.*']),
    # package_dir={'': 'medipt'},
    install_requires=['requirements.txt'],
    url='https://github.com/kleingeo/medipt',
    license='BSD 3-Clause',
    author='Geoff Klein',
    description='Medical Imaging Processing Tools'
)