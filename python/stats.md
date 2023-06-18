
## no `instance_group` or `dynamic_batching`

```bash
$ perf_analyzer -m text_recognition -b 1 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 6819
    Throughput: 378.807 infer/sec
    p50 latency: 42231 usec
    p90 latency: 42407 usec
    p95 latency: 42642 usec
    p99 latency: 42837 usec
    Avg HTTP time: 42221 usec (send/recv 28 usec + response wait 42193 usec)
  Server:
    Inference count: 6820
    Execution count: 6820
    Successful request count: 6820
    Avg request latency: 42095 usec (overhead 9 usec + queue 39460 usec + compute input 7 usec + compute infer 2614 usec + compute output 4 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 385.688 infer/sec, latency 5477 usec
Concurrency: 4, throughput: 383.742 infer/sec, latency 10681 usec
Concurrency: 6, throughput: 381.911 infer/sec, latency 15992 usec
Concurrency: 8, throughput: 377.863 infer/sec, latency 21539 usec
Concurrency: 10, throughput: 379.575 infer/sec, latency 26626 usec
Concurrency: 12, throughput: 379.974 infer/sec, latency 31959 usec
Concurrency: 14, throughput: 379.25 infer/sec, latency 37345 usec
Concurrency: 16, throughput: 378.807 infer/sec, latency 42642 usec
```

```bash
perf_analyzer -m text_recognition -b 2 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 6262
    Throughput: 695.716 infer/sec
    p50 latency: 45946 usec
    p90 latency: 46311 usec
    p95 latency: 46481 usec
    p99 latency: 46772 usec
    Avg HTTP time: 45982 usec (send/recv 29 usec + response wait 45953 usec)
  Server:
    Inference count: 12524
    Execution count: 6262
    Successful request count: 6262
    Avg request latency: 45786 usec (overhead 9 usec + queue 42916 usec + compute input 8 usec + compute infer 2848 usec + compute output 5 usec)


Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 704.267 infer/sec, latency 5948 usec
Concurrency: 4, throughput: 700.842 infer/sec, latency 11736 usec
Concurrency: 6, throughput: 697.952 infer/sec, latency 17534 usec
Concurrency: 8, throughput: 697.173 infer/sec, latency 23267 usec
Concurrency: 10, throughput: 696.284 infer/sec, latency 29125 usec
Concurrency: 12, throughput: 695.84 infer/sec, latency 34923 usec
Concurrency: 14, throughput: 695.483 infer/sec, latency 40663 usec
Concurrency: 16, throughput: 695.716 infer/sec, latency 46481 usec
```


## with `dynamic_batching`, no `instance_group` 

```bash
$ perf_analyzer -m text_recognition -b 1 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 27912
    Throughput: 1550.46 infer/sec
    p50 latency: 10308 usec
    p90 latency: 10401 usec
    p95 latency: 10428 usec
    p99 latency: 10803 usec
    Avg HTTP time: 10316 usec (send/recv 26 usec + response wait 10290 usec)
  Server:
    Inference count: 27912
    Execution count: 3489
    Successful request count: 27912
    Avg request latency: 10114 usec (overhead 32 usec + queue 4965 usec + compute input 27 usec + compute infer 5080 usec + compute output 9 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 384.358 infer/sec, latency 5420 usec
Concurrency: 4, throughput: 581.332 infer/sec, latency 6925 usec
Concurrency: 6, throughput: 706.778 infer/sec, latency 8536 usec
Concurrency: 8, throughput: 1026.71 infer/sec, latency 7831 usec
Concurrency: 10, throughput: 1419.02 infer/sec, latency 7217 usec
Concurrency: 12, throughput: 1386.49 infer/sec, latency 8748 usec
Concurrency: 14, throughput: 1371.46 infer/sec, latency 10276 usec
Concurrency: 16, throughput: 1550.46 infer/sec, latency 10428 usec
```

```bash
perf_analyzer -m text_recognition -b 2 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 13984
    Throughput: 1553.65 infer/sec
    p50 latency: 20569 usec
    p90 latency: 20693 usec
    p95 latency: 20753 usec
    p99 latency: 21126 usec
    Avg HTTP time: 20589 usec (send/recv 30 usec + response wait 20559 usec)
  Server:
    Inference count: 27968
    Execution count: 3496
    Successful request count: 13984
    Avg request latency: 20436 usec (overhead 18 usec + queue 15295 usec + compute input 23 usec + compute infer 5092 usec + compute output 7 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 723.946 infer/sec, latency 5599 usec
Concurrency: 4, throughput: 1028.03 infer/sec, latency 7844 usec
Concurrency: 6, throughput: 1205.57 infer/sec, latency 10018 usec
Concurrency: 8, throughput: 1559.31 infer/sec, latency 10351 usec
Concurrency: 10, throughput: 1556.32 infer/sec, latency 15474 usec
Concurrency: 12, throughput: 1549.19 infer/sec, latency 15560 usec
Concurrency: 14, throughput: 1549.2 infer/sec, latency 20732 usec
Concurrency: 16, throughput: 1553.65 infer/sec, latency 20753 usec
```


## with `dynamic_batching` and `instance_group` 

```bash
$ perf_analyzer -m text_recognition -b 1 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 28443
    Throughput: 1579.94 infer/sec
    p50 latency: 10277 usec
    p90 latency: 12441 usec
    p95 latency: 13525 usec
    p99 latency: 14495 usec
    Avg HTTP time: 10124 usec (send/recv 26 usec + response wait 10098 usec)
  Server:
    Inference count: 28443
    Execution count: 5403
    Successful request count: 28443
    Avg request latency: 9928 usec (overhead 29 usec + queue 3081 usec + compute input 25 usec + compute infer 6784 usec + compute output 9 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 531.342 infer/sec, latency 3828 usec
Concurrency: 4, throughput: 682.883 infer/sec, latency 7149 usec
Concurrency: 6, throughput: 942.519 infer/sec, latency 7883 usec
Concurrency: 8, throughput: 1092.77 infer/sec, latency 8861 usec
Concurrency: 10, throughput: 1227.76 infer/sec, latency 9522 usec
Concurrency: 12, throughput: 1464.75 infer/sec, latency 9394 usec
Concurrency: 14, throughput: 1424.86 infer/sec, latency 11575 usec
Concurrency: 16, throughput: 1579.94 infer/sec, latency 13525 usec
```

```bash
$ perf_analyzer -m text_recognition -b 2 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 17592
    Throughput: 1954.5 infer/sec
    p50 latency: 16352 usec
    p90 latency: 16492 usec
    p95 latency: 16577 usec
    p99 latency: 16991 usec
    Avg HTTP time: 16368 usec (send/recv 28 usec + response wait 16340 usec)
  Server:
    Inference count: 35184
    Execution count: 4398
    Successful request count: 17592
    Avg request latency: 16218 usec (overhead 21 usec + queue 8041 usec + compute input 27 usec + compute infer 8120 usec + compute output 8 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 911.596 infer/sec, latency 4579 usec
Concurrency: 4, throughput: 1101.92 infer/sec, latency 9248 usec
Concurrency: 6, throughput: 1325.45 infer/sec, latency 10702 usec
Concurrency: 8, throughput: 1500.63 infer/sec, latency 13288 usec
Concurrency: 10, throughput: 1827.48 infer/sec, latency 14128 usec
Concurrency: 12, throughput: 1939.71 infer/sec, latency 16140 usec
Concurrency: 14, throughput: 1952.72 infer/sec, latency 16532 usec
Concurrency: 16, throughput: 1954.5 infer/sec, latency 16577 usec
```




```bash
$ perf_analyzer -m text_recognition -b 2 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 10394
    Throughput: 1154.8 infer/sec
    p50 latency: 27695 usec
    p90 latency: 27750 usec
    p95 latency: 27923 usec
    p99 latency: 28214 usec
    Avg HTTP time: 27701 usec (send/recv 26 usec + response wait 27675 usec)
  Server:
    Inference count: 20788
    Execution count: 5197
    Successful request count: 10394
    Avg request latency: 27569 usec (overhead 12 usec + queue 24113 usec + compute input 16 usec + compute infer 3421 usec + compute output 6 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 740.055 infer/sec, latency 5466 usec
Concurrency: 4, throughput: 1172.12 infer/sec, latency 6863 usec
Concurrency: 6, throughput: 1164.58 infer/sec, latency 10565 usec
Concurrency: 8, throughput: 1160.14 infer/sec, latency 13875 usec
Concurrency: 10, throughput: 1155.03 infer/sec, latency 17614 usec
Concurrency: 12, throughput: 1155.91 infer/sec, latency 20859 usec
Concurrency: 14, throughput: 1155.47 infer/sec, latency 24287 usec
Concurrency: 16, throughput: 1154.8 infer/sec, latency 27923 usec
```


```bash
$ perf_analyzer -m text_recognition_trt -b 1 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 10800
    Throughput: 599.949 infer/sec
    p50 latency: 26713 usec
    p90 latency: 26915 usec
    p95 latency: 26930 usec
    p99 latency: 27339 usec
    Avg HTTP time: 26660 usec (send/recv 31 usec + response wait 26629 usec)
  Server:
    Inference count: 10800
    Execution count: 10800
    Successful request count: 10800
    Avg request latency: 26531 usec (overhead 10 usec + queue 23212 usec + compute input 2 usec + compute infer 1662 usec + compute output 1645 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 620.116 infer/sec, latency 3247 usec
Concurrency: 4, throughput: 613.227 infer/sec, latency 6550 usec
Concurrency: 6, throughput: 608.836 infer/sec, latency 9892 usec
Concurrency: 8, throughput: 606.614 infer/sec, latency 13202 usec
Concurrency: 10, throughput: 605.998 infer/sec, latency 16597 usec
Concurrency: 12, throughput: 604.728 infer/sec, latency 20049 usec
Concurrency: 14, throughput: 602.003 infer/sec, latency 23419 usec
Concurrency: 16, throughput: 599.949 infer/sec, latency 26930 usec
```


```bash
perf_analyzer -m text_recognition_trt -b 1 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 18292
    Throughput: 1016.12 infer/sec
    p50 latency: 15725 usec
    p90 latency: 15898 usec
    p95 latency: 15974 usec
    p99 latency: 16290 usec
    Avg HTTP time: 15740 usec (send/recv 36 usec + response wait 15704 usec)
  Server:
    Inference count: 18292
    Execution count: 3430
    Successful request count: 18292
    Avg request latency: 15532 usec (overhead 43 usec + queue 4995 usec + compute input 2 usec + compute infer 5318 usec + compute output 5173 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 206.208 infer/sec, latency 9822 usec
Concurrency: 4, throughput: 273.646 infer/sec, latency 14678 usec
Concurrency: 6, throughput: 408.745 infer/sec, latency 14709 usec
Concurrency: 8, throughput: 544.282 infer/sec, latency 14722 usec
Concurrency: 10, throughput: 675.056 infer/sec, latency 14833 usec
Concurrency: 12, throughput: 795.602 infer/sec, latency 15109 usec
Concurrency: 14, throughput: 911.455 infer/sec, latency 15456 usec
Concurrency: 16, throughput: 1016.12 infer/sec, latency 15974 usec
```

```bash
perf_analyzer -m text_recognition_trt -b 2 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95

Request concurrency: 16
  Client:
    Request count: 12978
    Throughput: 1441.85 infer/sec
    p50 latency: 22141 usec
    p90 latency: 22513 usec
    p95 latency: 22609 usec
    p99 latency: 22872 usec
    Avg HTTP time: 22197 usec (send/recv 37 usec + response wait 22160 usec)
  Server:
    Inference count: 25956
    Execution count: 2432
    Successful request count: 12978
    Avg request latency: 21817 usec (overhead 51 usec + queue 5703 usec + compute input 2 usec + compute infer 9582 usec + compute output 6478 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 410.307 infer/sec, latency 9773 usec
Concurrency: 4, throughput: 547.186 infer/sec, latency 14726 usec
Concurrency: 6, throughput: 792.83 infer/sec, latency 15203 usec
Concurrency: 8, throughput: 1024.36 infer/sec, latency 15764 usec
Concurrency: 10, throughput: 1191.02 infer/sec, latency 16977 usec
Concurrency: 12, throughput: 1410.18 infer/sec, latency 17230 usec
Concurrency: 14, throughput: 1316.97 infer/sec, latency 21465 usec
Concurrency: 16, throughput: 1441.85 infer/sec, latency 22609 usec
```


```bash
perf_analyzer -m text_recognition_trt -b 2 --shape input.1:1,32,100 --concurrency-range 2:16:2 --percentile=95


Request concurrency: 16
  Client:
    Request count: 13211
    Throughput: 1467.76 infer/sec
    p50 latency: 21801 usec
    p90 latency: 22033 usec
    p95 latency: 22076 usec
    p99 latency: 22409 usec
    Avg HTTP time: 21804 usec (send/recv 39 usec + response wait 21765 usec)
  Server:
    Inference count: 26410
    Execution count: 2476
    Successful request count: 13205
    Avg request latency: 21578 usec (overhead 36 usec + queue 6421 usec + compute input 2 usec + compute infer 8009 usec + compute output 7109 usec)

Inferences/Second vs. Client p95 Batch Latency
Concurrency: 2, throughput: 407.752 infer/sec, latency 9855 usec
Concurrency: 4, throughput: 541.737 infer/sec, latency 14845 usec
Concurrency: 6, throughput: 790.709 infer/sec, latency 15322 usec
Concurrency: 8, throughput: 1007.8 infer/sec, latency 16410 usec
Concurrency: 10, throughput: 1196.11 infer/sec, latency 17050 usec
Concurrency: 12, throughput: 1392.29 infer/sec, latency 17263 usec
Concurrency: 14, throughput: 1537.59 infer/sec, latency 18404 usec
Concurrency: 16, throughput: 1467.76 infer/sec, latency 22076 usec
```