import numpy as np
from PIL import Image
import io

CIFAR_FOLDER = "./data/cifar-10/train"

CIFAR_N = 50_000


def load_image(id):
    img = Image.open(f"{CIFAR_FOLDER}/{id}.png")
    return np.asarray(img)

def load_image_bin(id: int) -> bytes:
    with  open(f"{CIFAR_FOLDER}/{id}.png", "rb") as file:
        image = file.read()
        image = np.frombuffer(image, dtype=np.uint8)

        __image = Image.open(io.BytesIO(image.tobytes()))
        return image

def load_cifar(N: int, batch_size: int = 1):
    imgs = []
    for i in range(1, N + 1):
        imgs.append(load_image(i))
    return np.split(np.asarray(imgs), N // batch_size)

def load_cifar_bin(N: int, batch_size: int = 1):
    imgs = []
    for i in range(1, N + 1):
        imgs.append(load_image_bin(i))
    imgs = stack_image_arrays(imgs)
    return np.split(imgs, N // batch_size)

def stack_image_arrays(images: list[np.ndarray]) -> np.ndarray:
    max_width = max(img.shape[0] for img in images)
    for i in range(len(images)):
        pad_len = max_width - len(images[i])
        if pad_len > 0:
            images[i] = np.pad(images[i], (0, pad_len))
    images = np.vstack(images)
    return images

