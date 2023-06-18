#!/usr/bin/env bash

# run inside docker container
# 
# docker run -it --gpus all \
#    -v /var/run/docker.sock:/var/run/docker.sock \
#    -v ${PWD}:${PWD} \
#    --net=host nvcr.io/nvidia/tritonserver:23.05-py3-sdk

MODEL=cifar

PROJ_DIR=/home/m-nny/projects/ninetails

mkdir -p $PROJ_DIR/tmp
mkdir -p $PROJ_DIR/data/profile_results

model-analyzer profile \
    --model-repository $PROJ_DIR/model_repository \
    --profile-models $MODEL \
    --triton-launch-mode=docker \
    --output-model-repository-path $PROJ_DIR/tmp/output_model_repository \
    --override-output-model-repository \
    --latency-budget 40 \
    --export-path $PROJ_DIR/data/profile_results \
    --checkpoint-directory $PROJ_DIR/tmp/checkpoints \
    --run-config-search-mode quick