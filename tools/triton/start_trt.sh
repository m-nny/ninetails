#!/usr/bin/env bash

docker run -it --gpus all \
    -v ${PWD}/model_repository:/models \
    -e POLYGRAPHY_AUTOINSTALL_DEPS=1 \
    -v ${PWD}:${PWD} \
    --net=host nvcr.io/nvidia/tensorrt:23.05-py3