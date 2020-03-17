#!/usr/bin/env bash

update_packages() {
    echo "Updating packages"
    sudo apt update
    sudo apt upgrade
}

install_php() {
    echo "Installing PHP"
    sudo apt-get install software-properties-common
    sudo add-apt-repository ppa:ondrej/php
    sudo add-apt-repository ppa:ondrej/apache2
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y php7.3
    sudo systemctl restart apache2
}

install_python() {
    echo "Installing Python"
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt install python3.7
}

install_flask() {
    echo "Installing Flask"
    sudo mkdir /vagrant_data/MusifyApp
    cd /vagrant_data/MusifyApp
    update_packages
    sudo apt-get install python3-venv
    sudo python3 -m venv MusifyVenv
    source MusifyVenv/bin/activate
    sudo `which pip` install Flask
    deactivate
}

clean_up() {
    echo "Cleaning"
    sudo apt -y autoremove && sudo apt autoclean > /dev/null 2>&1
}

setup() {
    update_packages
    install_php
    install_python
    install_flask
    clean_up
}

setup "$@"
