#! /bin/sh

echo '>>> Enter the virtual environment'
. venv/bin/activate

echo '>>> Set up harness'
cd harness
    make
cd ..

echo '>>> Set up "crashes/" directory to store crashes'
mkdir crashes/

echo '>>> TODO Run actual fuzzer'
