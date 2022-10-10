#!/bin/bash
# 
# Load data fixtures from specified fixture directory.
#
# Author: Thomas Gwasira
# Date: 2022

FIXTURE_DIR="./fixtures"

cd $FIXTURE_DIR

for fixture_file in *.json; do
    django-admin loaddata $fixture_file
done