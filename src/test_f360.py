import os
import glob
import json

import cv2
import tensorflow as tf
import numpy as np

def main():
    #path_to_model = "trained_models/f360_vgg_01/"
    path_to_model = "trained_models/f360_MobileNetV2_04/"
    path_to_imgs = "datasets/test-report/"

    with open(path_to_model+"setup.json", "r") as data:
        setup = json.load(data)

    #w, h, _ = 100, 100, 3 #setup["input_shape"]
    w, h, _ = setup["input_shape"]
    classes = setup["classes"]

    print("[INFO] Loading model...")
    model = tf.keras.models.load_model(path_to_model+"model.h5")
    _ = input("[INFO] Click to continue")
    #model = tf.keras.models.load_model(path_to_model+"checkpoints/model_checkpoint_5.h5")
    img_folders = glob.glob(path_to_imgs + "*")
    img_paths = []
    for folder in img_folders:
        for i in glob.glob(folder + "/*"):
            img_paths.append(i)

    img_paths = glob.glob(path_to_imgs+"*")
    img_paths = sorted(img_paths)
    print(img_paths)

    i = 0
    
    for img_path in img_paths:
        image = cv2.imread(img_path)
        original_image = np.copy(image)

        image = tf.convert_to_tensor(image)
        image /= 255
        image = tf.image.resize(image, [w, h])
        image = tf.expand_dims(image, 0)

        prediction = model.predict(image)
        prediction *= 100.0
        prediction = tf.cast(prediction, tf.int8)
        print(prediction)
        index = tf.math.argmax(prediction, axis=1)
        index = tf.keras.backend.get_value(index)[0]

        cat = classes[index]
        print(cat)

        cv2.putText(original_image, cat , (10, 45),  cv2.FONT_HERSHEY_SIMPLEX,
                1.8, (0, 255, 0), 4)
        cv2.imshow("Test images", original_image)
        cv2.waitKey(0)
        cv2.imwrite(path_to_imgs+"res_{}.png".format(i), original_image)
        i += 1


main()
