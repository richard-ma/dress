#!/bin/sh

# install python3
`pwd`/install_python3.sh

# install virtualenv
pip install virtualenv

# create python3 virtualenv
virtualenv -p python3 dress
cd dress
. ./bin/activate

# download dress
wget -O dress.zip -c https://github.com/richard-ma/dress/archive/master.zip
unzip dress.zip
mv dress-master dress
rm -f dress.zip

# install requirements
pip install -r dress/requirements.txt

# create database
python dress/install.py

# run app
python dress/app.py
