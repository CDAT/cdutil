#!/usr/bin/env bash
ls
pwd
export PATH=${HOME}/miniconda/bin:${PATH}
conda install -c uvcdat/label/nightly -c conda-forge -c uvcdat nose cdms2 genutil cdat_info
export UVCDAT_ANONYMOUS_LOG=False
python setup.py install
