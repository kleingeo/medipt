Installation
==================

MedIPT is available for Python 3.7 to 3.11, and can be installed via pip or conda.

Installation via Anaconda
-------------------------

The easiest way to install **MedIPT** is with `Anaconda <https://anaconda.org/medipt/medipt>`_ and is available for all major OS platforms.

If **SimpleITK** is already installed, **MedIPT** can be installed with the following command:
.. code-block::

    conda install -c medipt medipt

Otherwise, `MedIPT` can be installed with the following command:
.. code-block::

    conda install -c medipt -c simpleitk -c medipt


On **Windows**, if **SimpleITK** is not installed, ensure **conda-forge** is being used to install.
.. code-block::

    conda install -c medipt -c simpleitk -c conda-forge medipt



Installation via pip
--------------------

Pip installation can be done by:
.. code-block::

    pip install -i https://pypi.anaconda.org/medipt/simple medipt

