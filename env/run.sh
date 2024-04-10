#!/bin/bash

# build the image
docker build -t mvg_image .

# run the container
docker run -it --rm mvg_image -e DISPLAY:$DISPLAY