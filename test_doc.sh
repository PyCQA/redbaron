#!/bin/bash

set +x

cd docs

result=$(make html 2>&1)

echo $result

if [ "$(echo $result | grep 'Exception in')"]
then
  exit 1
fi
