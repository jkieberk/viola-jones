import cv2
import numpy as np
from integralImage import integralImage
import os

def load_images(path, label):
    images = []
    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            images.append(integralImage(os.path.join(path, _file), label))
    return images

def main():
    #begin viola
    #Load faces images with label of 1
    faces = load_images("faces/", 1)
    #Load nonfaces imaegs with Label of 0
    faces = load_images("nonfaces/", 0)
    

if __name__ == "__main__":
    main()