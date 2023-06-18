# %%
#!%matplotlib inline
import pprint
import tempfile

from IPython import display
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow_datasets as tfds


import tensorflow_models as tfm

# These are not in the tfm public API for v2.9. They will be available in v2.10
from official.vision.serving import export_saved_model_lib
import official.core.train_lib

# %%
exp_config = tfm.core.exp_factory.get_exp_config("resnet_imagenet")
tfds_name = "cifar10"
ds_info = tfds.builder(tfds_name).info
ds_info
# %%
# Configure model
exp_config.task.model.num_classes = 10
exp_config.task.model.input_size = list(ds_info.features["image"].shape)
exp_config.task.model.backbone.resnet.model_id = 18

# Configure training and testing data
batch_size = 128

exp_config.task.train_data.input_path = ""
exp_config.task.train_data.tfds_name = tfds_name
exp_config.task.train_data.tfds_split = "train"
exp_config.task.train_data.global_batch_size = batch_size

exp_config.task.validation_data.input_path = ""
exp_config.task.validation_data.tfds_name = tfds_name
exp_config.task.validation_data.tfds_split = "test"
exp_config.task.validation_data.global_batch_size = batch_size
# %% Adjust the trainer configuration.
logical_device_names = [
    logical_device.name for logical_device in tf.config.list_logical_devices()
]

if "GPU" in "".join(logical_device_names):
    print("This may be broken in Colab.")
    device = "GPU"
elif "TPU" in "".join(logical_device_names):
    print("This may be broken in Colab.")
    device = "TPU"
else:
    print("Running on CPU is slow, so only train for a few steps.")
    device = "CPU"

if device == "CPU":
    train_steps = 20
    exp_config.trainer.steps_per_loop = 5
else:
    train_steps = 5000
    exp_config.trainer.steps_per_loop = 100

exp_config.trainer.summary_interval = 100
exp_config.trainer.checkpoint_interval = train_steps
exp_config.trainer.validation_interval = 1000
exp_config.trainer.validation_steps = ds_info.splits["test"].num_examples // batch_size
exp_config.trainer.train_steps = train_steps
exp_config.trainer.optimizer_config.learning_rate.type = "cosine"
exp_config.trainer.optimizer_config.learning_rate.cosine.decay_steps = train_steps
exp_config.trainer.optimizer_config.learning_rate.cosine.initial_learning_rate = 0.1
exp_config.trainer.optimizer_config.warmup.linear.warmup_steps = 100

# %%
pprint.pprint(exp_config.as_dict())

display.Javascript("google.colab.output.setIframeHeight('300px');")
# %%
logical_device_names = [logical_device.name for logical_device in tf.config.list_logical_devices()]

if exp_config.runtime.mixed_precision_dtype == tf.float16:
    tf.keras.mixed_precision.set_global_policy('mixed_float16')

if 'GPU' in ''.join(logical_device_names):
  distribution_strategy = tf.distribute.MirroredStrategy()
elif 'TPU' in ''.join(logical_device_names):
  tf.tpu.experimental.initialize_tpu_system()
  tpu = tf.distribute.cluster_resolver.TPUClusterResolver(tpu='/device:TPU_SYSTEM:0')
  distribution_strategy = tf.distribute.experimental.TPUStrategy(tpu)
else:
  print('Warning: this will be really slow.')
  distribution_strategy = tf.distribute.OneDeviceStrategy(logical_device_names[0])
# %%
with distribution_strategy.scope():
  model_dir = tempfile.mkdtemp()
  task = tfm.core.task_factory.get_task(exp_config.task, logging_dir=model_dir)

#  tf.keras.utils.plot_model(task.build_model(), show_shapes=True)
# %%
for images, labels in task.build_inputs(exp_config.task.train_data).take(1):
  print()
  print(f'images.shape: {str(images.shape):16}  images.dtype: {images.dtype!r}')
  print(f'labels.shape: {str(labels.shape):16}  labels.dtype: {labels.dtype!r}')
# %%
plt.hist(images.numpy().flatten());
# %%
label_info = ds_info.features['label']
label_info.int2str(1)
# %%
def show_batch(images, labels, predictions=None):
  plt.figure(figsize=(10, 10))
  min = images.numpy().min()
  max = images.numpy().max()
  delta = max - min

  for i in range(12):
    plt.subplot(6, 6, i + 1)
    plt.imshow((images[i]-min) / delta)
    if predictions is None:
      plt.title(label_info.int2str(labels[i]))
    else:
      if labels[i] == predictions[i]:
        color = 'g'
      else:
        color = 'r'
      plt.title(label_info.int2str(predictions[i]), color=color)
    plt.axis("off")
# %%
plt.figure(figsize=(10, 10))
for images, labels in task.build_inputs(exp_config.task.train_data).take(1):
  show_batch(images, labels)
plt.show()
# %% Train and evaluate
model, eval_logs = tfm.core.train_lib.run_experiment(
    distribution_strategy=distribution_strategy,
    task=task,
    mode='train_and_eval',
    params=exp_config,
    model_dir=model_dir,
    run_post_eval=True)

# %%
for key, value in eval_logs.items():
    if isinstance(value, tf.Tensor):
      value = value.numpy()
    print(f'{key:20}: {value:.3f}')
# %%
for images, labels in task.build_inputs(exp_config.task.train_data).take(1):
  predictions = model.predict(images)
  predictions = tf.argmax(predictions, axis=-1)

show_batch(images, labels, tf.cast(predictions, tf.int32))

if device=='CPU':
  plt.suptitle('The model was only trained for a few steps, it is not expected to do well.')
# %% export SavedModel
saved_model_path = './data/resnet-cifar'
export_saved_model_lib.export_inference_graph(
    input_type='image_tensor',
    batch_size=None,
    input_image_size=[32, 32],
    params=exp_config,
    checkpoint_path=tf.train.latest_checkpoint(model_dir),
    export_dir=saved_model_path)

# %%
# Importing SavedModel
imported = tf.saved_model.load(saved_model_path)
model_fn = imported.signatures['serving_default']
#%%
import numpy as np
plt.figure(figsize=(10, 10))
for data in tfds.load('cifar10', split='test').batch(12).take(1):
  predictions = []
  for image in data['image']:
    print("image", image[tf.newaxis, ...])
    index = tf.argmax(model_fn(image[tf.newaxis, ...])['logits'], axis=1)[0]
    predictions.append(index)
  print("predictions:", np.array(predictions))
  show_batch(data['image'], data['label'], predictions)

  if device=='CPU':
    plt.suptitle('The model was only trained for a few steps, it is not expected to do better than random.')
# %%
