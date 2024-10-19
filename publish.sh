#!/bin/bash

rm -rf .tmp

git clone . .tmp

git -C .tmp checkout gh-pages

rm -rf .tmp/*

cp -r web/* .tmp