# This has been tested on a new Ubuntu-14.04 vagrant box.
# If using anything else, YMMV.

# PS: You might need to ensure that there is enough memory
# given to the VM. I would suggest 2048MB or more.

# Install all requirements
sudo apt-get update
sudo apt-get install -y git make clang-3.5 realpath screen zlib1g-dev libssl-dev
sudo apt-get build-dep -y python3.4

# Ensure that the clang and clang++ executables point correctly
sudo update-alternatives --install /usr/bin/clang clang $(which clang-3.5) 100
sudo update-alternatives --install /usr/bin/clang++ clang++ $(which clang++-3.5) 100

# To prevent git from complaining
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8

# Set up the fuzzing-numpy repository
git clone /vagrant ~/fuzzing-numpy
cd ~/fuzzing-numpy
./first_run.sh
cd ..

# Set up symlink for crashes directory
cd ~/fuzzing-numpy
mkdir -p /vagrant/crashes
ln -s /vagrant/crashes ./crashes
cd ..

