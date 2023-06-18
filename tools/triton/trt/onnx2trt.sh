#!/usr/bin/env bash

# run inside docker container
# 
# docker run -it --gpus all \
#     -v /var/run/docker.sock:/var/run/docker.sock \
#     -v ./model_repository:/models \
#     --net=host nvcr.io/nvidia/tensorrt:23.05-py3

MODEL=text_recognition

trtexec --onnx=model.onnx \
        --saveEngine=model.plan \
        --explicitBatch