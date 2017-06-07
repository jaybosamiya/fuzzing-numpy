# Fuzzing Numpy
> :snake: Experimentations in trying to find 0-days in numpy

Inspired by Murmus CTF's
[live streams](https://www.youtube.com/playlist?list=PLfERMgzlCp0Czg0MiLrfyqrahHMmzsCI6) on
fuzzing numpy, I decided to write my own custom fuzzer as well, and
try to fuzz numpy.

This repository contains my explorations and experimentations in
trying to fuzz numpy. Over time, I might expand into fuzzing other
parts of CPython itself (or other libraries for Python).

## Usage

Run `./first_run.sh` to download and compile CPython and Numpy with
ASAN (address sanitizer).

Then, use `./wrapper.sh` to start the fuzzer, and watch the crashing
inputs get dropped into the `crashes` directory.

### Quick Start

It is possible to start off quickly by spinning up a new virtual
machine, and running the fuzzer inside it (it also would prevent any
unintended side-effects that might occur due to fuzzing).

This has been implemented as a `Vagrantfile` in this directory itself,
which runs an Ubuntu-14.04 virtual machine with all required
configuration etc, and auto-starts the fuzzing process into the
background whenever it boots. It can be booted simply by running
`vagrant up` inside this repository. Following this, running `vagrant
ssh` will let you access the box, where the running process can be
seen with `screen -r` (and disconnected without killing by pressing
Ctrl+a, d). To stop the fuzzer and the virtual machine, merely run
`vagrant halt`.

**Note:** Starting up the vagrant box also creates a `crashes/`
directory in the repository directory, which is symlinked inside the
virtual machine, so that the crashes can be obtained outside the VM
wiht ease.

## Structure of the Fuzzer

The fuzzer consists of multiple parts working in unison to lead to
effective finding of bugs.

1. We have the ASAN compilation for both CPython and numpy
   (see [`./first_run.sh`](/first_run.sh)). This allows us to catch
   even subtle errors (that might take longer to manifest as a crash),
   such as heap corruption etc.

2. We have a harness that handles crashing applications
   (see [`harness/harness.c`](harness/harness.c)). Specifically, it is
   compiled as a shared object (`.so` file) which is loaded into
   python using `ctypes` and it sets up signal handlers for SIGABRT
   (signifying an error caught by ASAN) and SIGSEGV (more serious
   error; missed by ASAN for some reason). It also uses an mmap'd
   region where testcases can be registered before running, thereby
   allowing the crashed process to be able to cleanly store the
   crashing input.

3. We have the the main fuzzer itself that handles repeatedly trying
   newly generated testcases and puts all the different parts of the
   fuzzer together (see [`fuzzer/main.py`](fuzzer/main.py)).

4. We have the generator, whose job is to keep track of the corpus,
   generate cases to test out, keep track of valid cases to increase
   corpus, etc. (see [`fuzzer/generator.py`](fuzzer/generator.py)).

5. We have the wrapper utility (see [`./wrapper.sh`](wrapper.sh))
   which repeatedly calls the fuzzer with the right configuration for
   ASAN etc, in order to get a whole host of bugs rather than stopping
   after just one bug that otherwise be done by the main fuzzer.
