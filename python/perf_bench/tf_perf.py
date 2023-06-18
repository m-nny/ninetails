# %%
import numpy as np
from dataset import load_cifar, CIFAR_N
from tqdm.auto import tqdm
import time

BATCH_SIZE = 1
N = 50_000

dataset = load_cifar(N, BATCH_SIZE)
# %%
import tensorflow as tf

imported = tf.saved_model.load("./data/resnet-cifar")
model_fn = imported.signatures["serving_default"]


# %%
def preprocess(image):
    return tf.convert_to_tensor(image)


def postprocess(pred):
    logits, probs = pred["logits"].numpy(), pred["probs"].numpy()
    index = np.argmax(logits, axis=1)
    return index, np.take_along_axis(probs, np.expand_dims(index, axis=-1), axis=1)


start_time = time.time()
for image in tqdm(dataset):
    image = preprocess(image)
    pred = model_fn(image)
    idx, prob = postprocess(pred)
end_time = time.time()
print(f"Processed {len(dataset)} in {end_time - start_time:.2f}s")
# %%
