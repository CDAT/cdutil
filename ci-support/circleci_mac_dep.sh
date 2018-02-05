#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda create -n py3 -c uvcdat/label/nightly -c conda-forge genutil nose flake8 "python>3" "numpy=1.13" netcdf-fortran=4.4.4=3
conda create -n py2 -c uvcdat/label/nightly -c conda-forge genutil nose flake8 "numpy=1.13" netcdf-fortran=4.4.4=3
export UVCDAT_ANONYMOUS_LOG=False
source activate py3
python setup.py install
source activate py2
rm -rf build
python setup.py install
