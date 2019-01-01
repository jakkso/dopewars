#!/usr/bin/env bash

docker run -it \
  -v /Users/Xander/python/DopeWars/scores.csv:/app/scores.csv \
  jakks/dopewars