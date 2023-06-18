#!/usr/bin/env bash

MODEL=text_recognition

PROJ_DIR=/home/m-nny/projects/ninetails

model-analyzer report \
    --model-repository $PROJ_DIR/model_repository \
    --profile-models $MODEL \
    --triton-launch-mode=docker \
    --output-model-repository-path $PROJ_DIR/output_model_repositryo \
    --override-output-model-repository \
    --latency-budget 10 \
    --run-config-search-mode quick