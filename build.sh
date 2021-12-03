#!/usr/bin/env bash

docker build -t parser-ndl:latest .
docker run --rm --name parse-ndl -v "$PWD/result":/parser/result parser-ndl:latest