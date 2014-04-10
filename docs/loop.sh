#!/bin/bash

while true; do clear; make html; sleep 0.1; inotifywait -e modify *.rst; done
