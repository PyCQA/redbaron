#!/bin/zsh

source ~/.zshrc

if [ -e "./test_distribution" ]; then
    rm -rf ./test_distribution
fi

mkdir test_distribution
cd test_distribution
mkvee
source ./ve/bin/active
upgrade_pip
pip install redbaron pytest
wget https://raw.githubusercontent.com/Psycojoker/redbaron/135071427967ee8cd97c3298da0b60a0923b7caa/tests/test_redbaron.py
py.test test_redbaron.py
