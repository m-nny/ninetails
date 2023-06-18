import numpy as np
from dataset import load_cifar_bin, CIFAR_N
from tqdm.auto import tqdm
import time
import tritonclient.http as httpclient
from multiprocessing import Pool

BATCH_SIZE = 1
N = 1


client = httpclient.InferenceServerClient(url="localhost:8000")

def preprocess(images):
    # images = images.reshape(BATCH_SIZE, -1)
    cifar_input = httpclient.InferInput("image_jpg", images.shape, datatype="UINT8")
    cifar_input.set_data_from_numpy(images)
    return cifar_input


def postprocess(res: httpclient.InferResult):
    # print('res', res.get_response())
    logits, probs = res.as_numpy("logits"), res.as_numpy("probs")
    index = np.argmax(logits, axis=1)
    return index, np.take_along_axis(probs, np.expand_dims(index, axis=-1), axis=1)

def infer(image):
    req = preprocess(image)
    # print(req)
    res = client.infer(model_name="cifar_ensemble", inputs=[req])
    post_res = postprocess(res)
    print(post_res)


start_time = time.time()
dataset = load_cifar_bin(N, BATCH_SIZE)

with Pool(4) as p:
    r = list(tqdm(p.imap(infer, dataset), total=len(dataset)))

# for r in tqdm(dataset):
#     infer(r)


end_time = time.time()
print(f"Processed {len(dataset)} in {end_time - start_time:.2f}s")
