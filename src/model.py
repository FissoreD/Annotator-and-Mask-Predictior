
from tensorflow import keras
from tensorflow.keras import layers
from global_vars import *
import tensorflow as tf
import os


def get_class_names():
    return os.listdir(crop_dir)


def make_model():
    data_augmentation = keras.Sequential(
        [
            layers.RandomFlip("horizontal",
                              input_shape=image_size+(3,)),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.1),
        ]
    )
    class_names = get_class_names()
    num_classes = len(class_names)

# Test model 7
    # model  = keras.models.Sequential([
    #     data_augmentation,
    #     layers.Rescaling(1./255),
    #     layers.Conv2D(16, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(16, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(32, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(32, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Dropout(0.2),
    #     layers.Flatten(),
    #     #layers.Dense(128, activation='relu'), py,
    #     layers.Dense(num_classes)
    # ])


# #Test model 6
#     model  = keras.models.Sequential([
#         data_augmentation,
#         layers.Rescaling(1./255),
#         layers.Conv2D(16, 4, padding='same', activation='relu'),
#         layers.MaxPooling2D(),
#         layers.Conv2D(16, 4, padding='same', activation='relu'),
#         layers.MaxPooling2D(),
#         layers.Conv2D(32, 4, padding='same', activation='relu'),
#         layers.MaxPooling2D(),
#         layers.Dropout(0.2),
#         layers.Flatten(),
#         #layers.Dense(128, activation='relu'), py,
#         layers.Dense(num_classes)
#     ])


# #Test model 5
    model = keras.models.Sequential([
        data_augmentation,
        layers.Rescaling(1./255),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        #layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.2),
        layers.Flatten(),
        #layers.Dense(128, activation='relu'), py,
        layers.Dense(num_classes)
    ])

# #Test model 4
#     model = keras.models.Sequential([
#         data_augmentation,
#         layers.Rescaling(1./255),
#         layers.Conv2D(16, 3, padding='same', activation='relu'),
#         layers.MaxPooling2D(2),
#         layers.Conv2D(32, 3, padding='same', activation='relu'),
#         layers.MaxPooling2D(2),
#         layers.Conv2D(64, 3, padding='same', activation='relu'),
#         layers.MaxPooling2D(),
#         layers.Conv2D(128, 3, padding='same', activation='relu'),
#         layers.MaxPooling2D(4),
#         layers.Dropout(0.2),
#         layers.BatchNormalization(),
#         layers.Flatten(),
#         #layers.Dense(128, activation='relu'),py,
#         layers.Dense(num_classes)

#     ])

    # Test model 3
    # model = keras.models.Sequential([
    #     data_augmentation,
    #     layers.Rescaling(1./255),
    #     layers.Conv2D(128, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(4),
    #     layers.Conv2D(64, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     #layers.Conv2D(64, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(2),
    #     layers.Dropout(0.4),
    #     layers.BatchNormalization(),
    #     layers.Flatten(),
    #     #layers.Dense(128, activation='relu'),py,
    #     layers.Dense(num_classes)

    # ])

    # Test model 2
    # model = keras.models.Sequential([
    #     data_augmentation,
    #     layers.Rescaling(1./255),
    #     layers.Conv2D(128, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(2),
    #     layers.Conv2D(32, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     #layers.Conv2D(64, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Dropout(0.2),
    #     layers.BatchNormalization(),
    #     layers.Flatten(),
    #     #layers.Dense(128, activation='relu'),py,
    #     layers.Dense(num_classes)

    # ])

    # Test model 1 - This model isn't good, the error is high
    # model = keras.models.Sequential([
    #     data_augmentation,
    #     layers.Rescaling(1./255),
    #     layers.Conv2D(16, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(2),
    #     layers.Conv2D(32, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(64, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Dropout(0.2),
    #     layers.BatchNormalization(),
    #     layers.Flatten(),
    #     #layers.Dense(128, activation='relu'),py,
    #     layers.Dense(num_classes)

    # ])

    f = tf.keras.losses.SparseCategoricalCrossentropy
    model.compile(optimizer='adam',
                  loss=f(from_logits=True),
                  metrics=['accuracy'])
    return model
