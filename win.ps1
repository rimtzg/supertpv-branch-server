#!/bin/bash

Copy-Item "app_config.ini" -Destination "$HOME/app_config.ini"

python main.py