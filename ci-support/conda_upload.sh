#!/usr/bin/env bash
PKG_NAME=genutil
USER=uvcdat
export PATH="$HOME/miniconda/bin:$PATH"
echo "Trying to upload conda"
if [ $(uname) == "Linux" ]; then
    OS=linux-64
    echo "Linux OS"
    conda update -y -q conda
    ESMF_CHANNEL="nesii/label/dev-esmf"
else
    echo "Mac OS"
    OS=osx-64
    ESMF_CHANNEL="nadeau1"
fi

mkdir ~/conda-bld
source activate root
conda install -q anaconda-client conda-build
conda config --set anaconda_upload no
export CONDA_BLD_PATH=${HOME}/conda-bld
export VERSION=$(date +%Y.%m.%d)
echo "Cloning recipes"
git clone git://github.com/UV-CDAT/conda-recipes
cd conda-recipes
# uvcdat creates issues for build -c uvcdat confises package and channel
rm -rf uvcdat
python ./prep_for_build.py -v $(date +%Y.%m.%d) -b py3
echo "Building and uploading now"
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.13 --python=2.7
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.12 --python=2.7
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.11 --python=2.7
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.10 --python=2.7
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.9 --python=2.7
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.13 --python=3.6
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.12 --python=3.6
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.11 --python=3.6
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.10 --python=3.6
conda build  -c uvcdat/label/nightly -c conda-forge -c ${ESMF_CHANNEL} -c uvcdat ${PKG_NAME} --numpy=1.9 --python=3.6
anaconda -t $CONDA_UPLOAD_TOKEN upload -u $USER -l nightly $CONDA_BLD_PATH/$OS/$PKG_NAME-$(date +%Y.%m.%d)-*_0.tar.bz2 --force
