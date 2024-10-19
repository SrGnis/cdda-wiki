#!/bin/bash

# Delete .tmp directory
rm -rf .tmp

# Prepare a directory with the source data
git clone . .tmp

# Checkout to the commit with the original data
git -C .tmp checkout 3e5ca38ff582623df5630dfa4e8a47d4a6bff28c

# Run the script to clean the data
python3 cleaning.py .tmp/web

# Delete the actual data
rm -rf web

# Moeve the cleaned data into the main repo
mv .tmp/web ./
