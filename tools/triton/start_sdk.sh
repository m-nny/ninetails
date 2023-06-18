#!/usr/bin/env bash

docker run -it --gpus all \
   -v /var/run/docker.sock:/var/run/docker.sock \
   -v ${PWD}:${PWD} \
   --net=host nvcr.io/nvidia/tritonserver:23.05-py3-sdk
