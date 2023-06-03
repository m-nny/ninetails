#!/usr/bin/env bash

INPUT=$1

plumber write rabbit \
    --exchange-name="test-exchange" \
    --routing-key="test-key" \
    --protobuf-dirs proto \
    --protobuf-root-message job.SumJobInput \
    --encode-type jsonpb \
    --input "$INPUT"