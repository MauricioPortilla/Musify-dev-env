# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "bento/ubuntu-18.04"
  config.vm.define "Musify-dev-env"
  config.vm.hostname = "Musify-dev-env"

  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "public_network", type: "dhcp"

  config.vm.synced_folder "./Musify", "/home/vagrant/Musify"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
    vb.customize [ "modifyvm", :id, "--uartmode1", "disconnected" ]
  end
  
  config.vm.provision :shell, privileged: false, run: 'once', path: 'provision/box_setup.sh', keep_color: true
end
