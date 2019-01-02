#!/usr/bin/env bash

docker build -t jakks/dopewars .
docker container prune -f
docker rmi $(docker images -qa -f 'dangling=true')