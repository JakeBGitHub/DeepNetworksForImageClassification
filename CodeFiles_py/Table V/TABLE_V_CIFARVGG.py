# -*- coding: utf-8 -*-
"""TABLE_V_CIFARVGG.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bAtKLY7TqkiSCsfwjjAr9ceNYFUet0GU
"""

# !pip install --upgrade tensorflow
# !pip install tensorflow==1.4

import tensorflow as tf
from tensorflow.keras import datasets, layers, models, optimizers, callbacks
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import regularizers
import matplotlib.pyplot as plt

cifar_shape = (32,32,3)
cifar_classes = 10

model_D = models.Sequential()

model_D.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=cifar_shape))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(64, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.MaxPool2D((2, 2), strides=2, padding='same'))

model_D.add(layers.Conv2D(128, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(128, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.MaxPool2D((2, 2), strides=2, padding='same'))

model_D.add(layers.Conv2D(256, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(256, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(256, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.MaxPool2D((2, 2), strides=2, padding='same'))

model_D.add(layers.Conv2D(512, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(512, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(512, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.MaxPool2D((2, 2), strides=2, padding='same'))

model_D.add(layers.Conv2D(512, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(512, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.Conv2D(512, (3, 3), padding='same', activation='relu'))
model_D.add(layers.BatchNormalization())
model_D.add(layers.MaxPool2D((2, 2), strides=2, padding='same'))
model_D.add(layers.Dropout(0.5))

model_D.add(layers.Flatten())
model_D.add(layers.Dense(4096, activation='relu'))
model_D.add(layers.Dense(4096, activation='relu'))
model_D.add(layers.Dense(cifar_classes, activation='softmax'))

model_D.summary()
# Total params: 138,357,544 for ILSVRC
# Total params: 33,638,218 for CIFAR
# Total params: 33,637,066 for MNIST

import tensorflow as tf
from tensorflow.keras import datasets
import matplotlib.pyplot as plt

(train_images_cifar, train_labels_cifar), (test_images_cifar, test_labels_cifar) = datasets.cifar10.load_data()

# Normalize pixel values to be between 0 and 1
train_images_cifar, test_images_cifar = train_images_cifar / 255.0, test_images_cifar / 255.0


print('train_images_cifar:', train_images_cifar.shape)
print('train_labels_cifar:', train_labels_cifar.shape)
print('test_images_cifar:', test_images_cifar.shape)
print('test_labels_cifar:', test_labels_cifar.shape)

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer',
               'dog', 'frog', 'horse', 'ship', 'truck']

plt.figure(figsize=(20,20))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images_cifar[i], cmap=plt.cm.binary)
    # The CIFAR labels happen to be arrays, 
    # which is why you need the extra index
    plt.xlabel(class_names[train_labels_cifar[i][0]])
plt.show()

sgd = optimizers.SGD(learning_rate=0.005, decay=1e-6, momentum=0.9, nesterov=True)

model_D.compile(optimizer=sgd,
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])


history = model_D.fit(train_images_cifar, 
                      train_labels_cifar, 
                      batch_size=256,
                      epochs=200,
                      validation_data=(test_images_cifar, test_labels_cifar))

plt.plot(history.history["accuracy"])
plt.plot(history.history['val_accuracy'])
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("model accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Accuracy","Validation Accuracy","loss","Validation Loss"])
plt.show()