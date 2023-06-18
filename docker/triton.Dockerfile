FROM nvcr.io/nvidia/tritonserver:23.05-py3

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torchvision opencv-python-headless

CMD ["tritonserver",  "--model-repository=/models"]