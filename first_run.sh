#! /bin/sh -x

echo '>>> Initialize the submodules'
git submodule init
git submodule update

echo '>>> Set up config options'
export CC="$(which clang) -g3 -fsanitize=address"
export CXX="$(which clang++) -g3 -fsanitize=address"

echo '>>> Set up cpython'
mkdir py
cd cpython
    ./configure --without-pydebug --prefix=$(realpath $(pwd)/../py)
    make -j$(nproc)
    make install
cd ..

echo '>>> Set up virtualenv'
py/bin/python3 -m venv venv

echo '>>> Activate virtualenv (from now on: python, pip etc will be in venv)'
source venv/bin/activate

echo '>>> Set up numpy'
pip install numpy
