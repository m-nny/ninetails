## Tensorflow naive inference

```bash
python ./python/perf_bench/tf_perf.py

Processed 50000 in 119.56s
```


## Triton ONNX with batch_size=1
`max_batch_size: 1`
```bash
python ./python/perf_bench/triton_perf.py

Processed 50000 in 68.43s
```


`max_batch_size: 2`
```bash
python ./python/perf_bench/triton_perf.py

Processed 50000 in 68.43s
```