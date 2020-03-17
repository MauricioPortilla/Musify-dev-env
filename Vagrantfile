# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "Musify-dev-env"
  config.vm.define "Musify-dev-env"
  config.vm.hostname = "Musify-dev-env"

  config.vm.network "forwarded_port", guest: 5000, host: 8080

  config.vm.network "public_network", ip: "192.168.26.2"

  config.vm.synced_folder "./data", "/vagrant_data"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
  end
  
  config.vm.provision :shell, privileged: false, run: 'once', path: 'provision/box_setup.sh', keep_color: true
end
