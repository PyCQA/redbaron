#!/bin/bash

set +x

if [ "$(python --version | grep 2.6)" ]
then
    exit 0
fi

pip install -r requirements-docs.txt

cd docs
rm -rf _build

result=$(make html 2>&1)

echo $result

if [ "$(echo $result | grep 'Exception in')" ]
then
  exit 1
fi
