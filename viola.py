import cv2
import numpy as np
from integralImage import integralImage
import os

def load_images(path, label):
    images = []
    i = 1
    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            images.append(integralImage(os.path.join(path, _file), label))
            print 'Image ' + str(i) + ' loaded'
            i = i + 1
    return images

def main():
    #begin viola
    #Load faces images with label of 1
    print 'Loading faces'
    faces = load_images("faces/", 1)
    #Load nonfaces imaegs with Label of 0
    print 'Loading non-faces'
    faces = load_images("nonfaces/", 0)
    print 'Loaded face & nonface image'

if __name__ == "__main__":
    main()