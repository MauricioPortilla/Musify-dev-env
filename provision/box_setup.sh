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

clean_up() {
    echo "Cleaning"
    sudo apt -y autoremove && sudo apt autoclean > /dev/null 2>&1
}

setup() {
    update_packages
    install_php
    install_python
    clean_up
}

setup "$@"
