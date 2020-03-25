#!/usr/bin/env bash

update_packages() {
    echo "Updating packages"
    sudo apt-get update -y
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
    sudo apt-get install -y python3 > /dev/null 2>&1
    sudo apt-get install -y python3-pip > /dev/null 2>&1
    sudo apt-get install -y python3-venv > /dev/null 2>&1
}

install_flask() {
    echo "Installing Flask"
    cd Musify
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    #deactivate
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
