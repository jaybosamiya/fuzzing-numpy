# Fuzzing Numpy
> :snake: Experimentations in trying to find 0-days in numpy

Inspired by Murmus CTF's [live streams](https://www.youtube.com/playlist?list=PLfERMgzlCp0Czg0MiLrfyqrahHMmzsCI6) on fuzzing numpy, I decided to write my own custom fuzzer as well, and try to fuzz numpy.

This repository contains my explorations and experimentations in trying to fuzz numpy. Over time, I might expand into fuzzing other parts of CPython itself (or other libraries for Python).

## Usage

Run `./first_run.sh` to download and compile CPython and Numpy with
ASAN (address sanitizer).

Then, use `wrapper.sh` to start the fuzzer, and watch the crashing
inputs get dropped into the `crashes` directory.
