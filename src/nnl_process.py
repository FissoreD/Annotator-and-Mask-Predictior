import os
import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import read_write
import images
import tags
import numpy as np
from global_vars import *
from model import *
"""
A lot of code of this file is inspired from the following internet page :
https://keras.io/examples/vision/image_classification_from_scratch/
"""


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


def train_model(train_ds, val_ds, model):
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs
    )
    if not os.path.exists(KERA_PRED_FOLDER):
        os.mkdir(KERA_PRED_FOLDER)
    read_write.clear_floder(KERA_PRED_FOLDER)
    model.save(KERA_PRED_FOLDER+'/model.h5', save_format='h5')
    return history


def predict(model, img_path, isProba=True, toPrint=False):
    """
    Make a prediction on an image
    isProba -> optional if we search the probability for each class or the category [default set to True]
    toPrint -> optional if we want to print on stdout the result of prediction [default set to False]
    """
    class_names = get_class_names()
    img = tf.keras.utils.load_img(img_path, target_size=image_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    its_class = class_names[np.argmax(score)]
    its_score = np.max(score)
    if toPrint:
        if isProba:
            print(
                "This image most likely belongs to {} with a {} percent confidence."
                .format(class_names, score)
            )
        else:
            print(
                "This image most likely belongs to {} with a {:.2f} percent confidence."
                .format(its_class, its_score*100)
            )
    return (its_class, its_score) if not isProba else (class_names, score)


def train_the_model():

    # Creation of training and validation set
    train_ds, val_ds = create_data_set(crop_dir)

    # Configure the dataset for performance
    train_ds, val_ds = configure_for_performance(train_ds, val_ds)

    model = make_model()

    history = train_model(train_ds, val_ds, model)
    return model, history


def read_model():
    return keras.models.load_model(KERA_PRED_FOLDER+"/model.h5")


def rename_test_img():
    diff = 0
    for pos, file_name in enumerate(os.listdir(test_img)):
        no = 'No'
        if file_name[0] == 'M':
            diff += 1
            no = ''
        else:
            pos -= diff
        name = f"{no}Mask_{pos}.jpg"
        os.rename(
            os.path.join(test_img, file_name),
            os.path.join(test_img, name))


def test_all(model):
    """
    Make a prediction on every file in test_img folder,
    printing the result in STDOUT
    """
    L = [('File name', 'Res', 'Proba')]
    length = map(len, L[0])
    for file_name in os.listdir(test_img):
        path = f"{test_img}/{file_name}"
        res, proba = predict(model, path, isProba=False)
        proba = "{:.2f}".format(float(proba))
        tup = f"![{file_name}]({path})", res, proba
        length = map(max, zip(length, map(len, tup)))
        L.append(tup)
    length = list(length)
    print(length)
    for pos, i in enumerate(L):
        print("| {: <{}} | {: <{}} | {: <{}} |".format(
            *[item for sublist in zip(i, length) for item in sublist]
        ))
        if pos == 0:
            print("| {} | {} | {} |".format(*['-' * i for i in length]))


if __name__ == "__main__":
    is_create_model = False or len(sys.argv) > 1
    if is_create_model:
        """
        Creation of images with annotation from file
        for testing phase
        """
        tag_list = tags.Tag(images.open_files())
        img_list = tag_list.imgs

        for j in img_list:
            j.set_tag_list(tag_list)

        read_write.read_file(img_list, file_path=json_test)
        read_write.create_all_cropped_images(img_list)

        model, history = train_the_model()
    else:
        model = read_model()

    # image_path = test_img + '/Mask_0.jpg'
    # predict(model, image_path, toPrint=True)
    test_all(model)

    """
    Here we test all images wrt our model
    """
    # test_all()
