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

echo '>>> Set up long-run killer (WARNING: Will kill all python processes every few seconds)'
touch DELETE_THIS_TO_STOP_KILLER
while true; do
    sleep 30
    if test -e DELETE_THIS_TO_STOP_KILLER; then
        killall python
    else
        break
    fi
done &

echo '>>> Run actual fuzzer'
while true; do
      python fuzzer/main.py
done
