#!/bin/bash

# build the image
docker build -t mvg_image -f Dockerfile ..

# run the container
docker run -it --rm -e DISPLAY=$DISPLAY mvg_image 