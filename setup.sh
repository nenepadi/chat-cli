#!/bin/bash

cp -rf /vagrant/chat-cli/ /home/vagrant/chat-cli

VIRTUALENV_DIR=/home/vagrant/.virtualenvs/chat-cli
PROJECT_DIR=/home/vagrant/chat-cli
VIRTUALENV_NAME=chat-cli

echo "Installing pip"

curl -s https://bootstrap.pypa.io/get-pip.py | python2.7 > /dev/null 2>&1

echo "Mysql Setup"
debconf-set-selections <<< "mysql-server mysql-server/root_password password admin"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password admin"
apt-get update
apt-get install -y mysql-server

# Setting up MySQL user and db
mysql -uroot -padmin -e "CREATE DATABASE IF NOT EXISTS chatcli" >> /home/vagrant/chat-cli/vm_build.log 2>&1
mysql -uroot -padmin -e "USE chatcli" >> /home/vagrant/cli-chat/vm_build.log 2>&1
mysql -uroot -padmin -e "CREATE TABLE IF NOT EXISTS chatcli.users ( \
    id int(11) NOT NULL AUTO_INCREMENT, \
    username varchar(255) NOT NULL, \
    PRIMARY KEY (id), \
    UNIQUE (username) \
    ) \
    AUTO_INCREMENT=1;" >> /home/vagrant/cli-chat/vm_build.log 2>&1
mysql -uroot -padmin -e "CREATE TABLE IF NOT EXISTS chatcli.messages ( \
    id int(11) NOT NULL AUTO_INCREMENT, \
    username varchar(255) NOT NULL, \
    message varchar(255) NOT NULL, \
    sender varchar(255) NOT NULL, \
    PRIMARY KEY (id) \
    ) \
    AUTO_INCREMENT=1;" >> /home/vagrant/cli-chat/vm_build.log 2>&1

echo 'Installing and configuring virtualenvwrapper...'
pip install --quiet virtualenvwrapper

# setting up virtualenv & installing requirements
su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR --python=/usr/bin/python2.7 && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    $VIRTUALENV_DIR/bin/pip install -r /vagrant/requirements.txt"

printf "export WORKON_HOME=/home/vagrant/.virtualenvs\n" >> /home/vagrant/.bashrc
printf "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7\n" >> ~vagrant/.bashrc
printf "source /usr/local/bin/virtualenvwrapper.sh\n" >> ~vagrant/.bashrc
echo "workon $VIRTUALENV_NAME" >> /home/vagrant/.bashrc

su - vagrant -c "source $VIRTUALENV_DIR/bin/activate"