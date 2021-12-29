import io
import os
from tkinter import Scrollbar
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import read_write
import matplotlib.pyplot as plt
import images
import tags
"""
A lot of code of this file is inspired from the following internet page : 
https://keras.io/examples/vision/image_classification_from_scratch/
"""

image_size = (180, 180)
KERA_PRED_FOLDER = 'keras_pred_folder'


def remove_not_valid_images(path):
    """ 
    This function aim to remove corrupted images (those whose name does not start with JFIF) 
    """
    try:
        fobj = open(path, "rb")
        is_jfif = tf.compat.as_bytes("JFIF") in fobj.peek(10)
    finally:
        fobj.close()

    if not is_jfif:
        os.remove(path)


def create_standardize_data_set(path):
    """
    Create training and validation standardize model from a path
    """
    def func(kwargs):
        return tf.keras.preprocessing.image_dataset_from_directory(path, **kwargs).prefetch(buffer_size=32)
    dico = {
        "validation_split": 0.2,
        "seed": 1337,
        "image_size": image_size,
        "batch_size": 32
    }
    train_ds = func(dict(dico, **{"subset": "training"}))
    val_ds = func(dict(dico, **{"subset": "validation"}))
    return train_ds, val_ds


def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)
    # Image augmentation block
    data_augmentation = keras.Sequential(
        [layers.RandomFlip("horizontal"), layers.RandomRotation(0.1), ]
    )
    x = data_augmentation(inputs)

    # Entry block
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)


def train_model(model, train_ds, val_ds):
    epochs = 50
    if not os.path.exists(KERA_PRED_FOLDER):
        os.mkdir(KERA_PRED_FOLDER)
    callbacks = [
        keras.callbacks.ModelCheckpoint("{folder}/save_at_{epoch}.h5"),
    ]
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    model.fit(
        train_ds, epochs=epochs, callbacks=callbacks, validation_data=val_ds,
    )


def evaluate_image(model, img_path):
    img = keras.preprocessing.image.load_img(
        img_path,
        target_size=image_size
    )

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)
    score = predictions[0]
    return score


if __name__ == "__main__":
    create_model = False
    if create_model:
        """ 
        Creation of images with annotation from file 
        for testing phase
        """
        tag_list = tags.Tag(images.open_files())
        img_list = tag_list.imgs

        for j in img_list:
            j.set_tag_list(tag_list)

        read_write.read_file(img_list, file_path="annotation/test.json")
        read_write.create_all_cropped_images(img_list)

        """
        Creation of training and validation set
        """
        train_ds, val_ds = create_standardize_data_set('crop_img')

        model = make_model(input_shape=image_size + (3,), num_classes=2)

        train_model(model, train_ds, val_ds)
    else:
        model = keras.models.load_model(KERA_PRED_FOLDER + '/save_at_50.h5')
    """
    Here we test an image with our model
    """
    score = evaluate_image(model, "crop_img/Mask/image5-bb-157x24-43-42.jpg")
    print(
        "This image is %.2f percent cat and %.2f percent dog."
        % (100 * (1 - score), 100 * score)
    )
