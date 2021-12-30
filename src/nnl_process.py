import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import read_write
import images
import tags
import numpy as np
"""
A lot of code of this file is inspired from the following internet page : 
https://keras.io/examples/vision/image_classification_from_scratch/
"""

image_size = (180, 180)
crop_dir = 'crop_img'
epochs = 10
KERA_PRED_FOLDER = 'keras_pred_folder'
MODEL_PATH = f"{KERA_PRED_FOLDER}/model"


def get_class_names():
    return os.listdir(crop_dir)


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


def create_data_set(path):
    """
    Create training and validation standardize model from path
    """
    def func(kwargs):
        return tf.keras.preprocessing.image_dataset_from_directory(path, **kwargs)
    dico = {
        "validation_split": 0.2,
        "seed": 1337,
        "image_size": image_size,
        "batch_size": 32
    }
    train_ds = func(dict(dico, **{"subset": "training"}))
    val_ds = func(dict(dico, **{"subset": "validation"}))
    return train_ds, val_ds


def configure_for_performance(train_ds, val_ds):
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return train_ds, val_ds


def normalize_train_ds(train_ds):
    normalization_layer = layers.Rescaling(1./255)
    return train_ds.map(lambda x, y: (normalization_layer(x), y))


def make_model():
    class_names = get_class_names()
    num_classes = len(class_names)
    model = keras.models.Sequential([
        layers.Rescaling(1./255, input_shape=image_size + (3,)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])
    f = tf.keras.losses.SparseCategoricalCrossentropy
    model.compile(optimizer='adam',
                  loss=f(from_logits=True),
                  metrics=['accuracy'])
    return model


def train_model(train_ds, val_ds, model):
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    model.save(MODEL_PATH)


def evaluate_image(model, img_path, toPrint=False):
    class_names = get_class_names()
    img = tf.keras.utils.load_img(img_path, target_size=image_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    its_class = class_names[np.argmax(score)]
    its_score = 100 * np.max(score)
    if toPrint:
        print(
            "This image most likely belongs to {} with a {:.2f} percent confidence."
            .format(its_class, its_score)
        )
    return its_class, its_score


def draw_a_plot_of_data(train_ds):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(train_ds.class_names[labels[i]])
            plt.axis("off")


def make_all():

    # Creation of training and validation set
    train_ds, val_ds = create_data_set(crop_dir)

    # Configure the dataset for performance
    train_ds, val_ds = configure_for_performance(train_ds, val_ds)

    normalized_ds = normalize_train_ds(train_ds)
    model = make_model()

    train_model(normalized_ds, val_ds, model)


if __name__ == "__main__":
    is_create_model = False
    if is_create_model:
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

        make_all()
    else:
        model = keras.models.load_model(
            f"{KERA_PRED_FOLDER}/model")

    image_path = 'crop_img/No/image_000-bb-15x0-307-431.jpg'
    evaluate_image(model, image_path)

    """
    Here we test all images wrt our model
    """
    for under_dir in os.listdir(crop_dir):
        for file_name in os.listdir(crop_dir+"/"+under_dir):
            path = f"{crop_dir}/{under_dir}/{file_name}"
            print(f"{under_dir} {file_name} {evaluate_image(model,path)}")
