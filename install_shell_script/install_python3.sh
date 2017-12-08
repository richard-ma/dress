#!/bin/sh

# enable epel repo
yum install -y epel-release
yum update -y

# install python3
yum install -y python34

# install pip
curl -O https://bootstrap.pypa.io/get-pip.py
/usr/bin/python3 get-pip.py

# install virtualenv
pip install virtualenv
