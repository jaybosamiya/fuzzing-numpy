# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what
# you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_check_update = false
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end

  config.vm.provision "shell",
                      path: "vagrant-provision.sh",
                      privileged: false

  config.vm.provision "shell",
                      inline: "cd ~/fuzzing-numpy; screen -d -m ./wrapper.sh",
                      privileged: false,
                      run: "always"

end
