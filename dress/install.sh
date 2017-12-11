#!/bin/sh

# config.DevelopmentConfig
# config.ProductionConfig
# config.TestingConfig
export APP_CONFIG='config.DevelopmentConfig'

python ./install.py
