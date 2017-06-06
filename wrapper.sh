#! /bin/sh

echo '>>> Enter the virtual environment'
. venv/bin/activate

echo '>>> Set up harness'
cd harness
    make
cd ..

echo '>>> Set up "crashes/" directory to store crashes'
mkdir crashes/

echo '>>> Set up ASAN configuration options'
export ASAN_OPTIONS=handle_segv=0,abort_on_error=1
# handle_segv=0     == allows user to set their own handler (needed for harness)
# abort_on_error=1  == causes a SIGABRT upon ASAN error (needed for harness)

echo '>>> TODO Run actual fuzzer'
