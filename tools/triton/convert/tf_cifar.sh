#!/usr/bin/env bash

SAVED_MODEL=./data/resnet-cifar
OUTPUT_ONNX_MODEL=./model_repository/cifar/1/model.onnx


python -m tf2onnx.convert \
   --saved-model $SAVED_MODEL \
   --output $OUTPUT_ONNX_MODEL