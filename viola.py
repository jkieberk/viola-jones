import cv2
import numpy as np
from integralImage import integralImage
import os
import pickle

def store_integral_images(path, label):
    images = []
    i = 1
    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            images.append(integralImage(os.path.join(path, _file), label))
            print 'Image ' + str(i) + ' loaded'
            i = i + 1
    store_integrals(images, label)

def load_integral_images():
    f = open('INTEGRALFACES ', 'r')
    with f as input:
        images = pickle.load(input)

def store_integrals(images, label):
    if label == 1:
        f = open('INTEGRALFACES ', 'w')
    else:
        f = open('INTEGRALNONFACES', 'w')
    with f as output:
        pickle.dump(images, output, pickle.HIGHEST_PROTOCOL)


def main():
    # #begin viola
    # #Load faces images with label of 1
    print 'Loading faces'
    faces = store_integral_images("faces/", 1)
    # #Load nonfaces imaegs with Label of 0
    print 'Loading non-faces'
    faces = store_integral_images("nonfaces/", 0)
    print 'Loaded face & nonface image'
    # load_integral_images()
if __name__ == "__main__":
    main()
