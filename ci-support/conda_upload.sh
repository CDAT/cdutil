#!/usr/bin/env bash
PKG_NAME=cdutil
USER=cdat
VERSION="8.0"
export PATH="$HOME/miniconda/bin:$PATH"
echo "Trying to upload conda"
if [ $(uname) == "Linux" ]; then
    OS=linux-64
    echo "Linux OS"
else
    echo "Mac OS"
    OS=osx-64
fi

conda update -y -q conda

mkdir ~/conda-bld
source activate root
conda install -q anaconda-client conda-build
conda config --set anaconda_upload no
export CONDA_BLD_PATH=${HOME}/conda-bld
echo "Cloning recipes"
git clone git://github.com/UV-CDAT/conda-recipes
cd conda-recipes
# uvcdat creates issues for build -c uvcdat confises package and channel
rm -rf uvcdat
python ./prep_for_build.py
echo "Building and uploading now"
conda build  -c cdat/label/nightly -c conda-forge -c cdat ${PKG_NAME} --python=2.7
conda build  -c cdat/label/nightly -c conda-forge -c cdat ${PKG_NAME} --python=3.6
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-${VERSION}.$(date +%Y.%m.%d)*_0.tar.bz2 --force
