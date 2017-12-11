#!/bin/sh

# config.DevelopmentConfig
# config.ProductionConfig
# config.TestingConfig
export APP_CONFIG='config.DevelopmentConfig'
export APP_SECRET_KEY='your secret key'

# create database
python ./install.py
