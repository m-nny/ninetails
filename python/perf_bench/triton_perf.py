import numpy as np
from dataset import load_cifar, CIFAR_N
from tqdm.auto import tqdm
import time
import tritonclient.http as httpclient
from multiprocessing import Pool

BATCH_SIZE = 1
N = 50_000


client = httpclient.InferenceServerClient(url="localhost:8000")

def preprocess(image):
    cifar_input = httpclient.InferInput("inputs", image.shape, datatype="UINT8")
    cifar_input.set_data_from_numpy(image)
    return cifar_input


def postprocess(res):
    logits, probs = res.as_numpy("logits"), res.as_numpy("probs")
    index = np.argmax(logits, axis=1)
    return index, np.take_along_axis(probs, np.expand_dims(index, axis=-1), axis=1)

def infer(image):
    req = preprocess(image)
    res = client.infer(model_name="cifar", inputs=[req])
    idx, prob = postprocess(res)


start_time = time.time()
dataset = load_cifar(N, BATCH_SIZE)

with Pool(4) as p:
    r = list(tqdm(p.imap(infer, dataset), total=len(dataset)))

# for r in tqdm(dataset):
#     infer(r)
end_time = time.time()
print(f"Processed {len(dataset)} in {end_time - start_time:.2f}s")
