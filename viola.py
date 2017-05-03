import cv2
import numpy as np
from integralImage import integralImage
from ada import train
import os
import pickle

def testImages(classifiers, image):
    return 1 if sum([c[0].get_vote(image) * np.log(1/c[1]) for c in classifiers]) >= 0 else -1
    
def store_integral_images(path, label):
    images = []
    i = 1
    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            if i < 500:
                images.append(integralImage(os.path.join(path, _file), label))
                print 'Image ' + str(i) + ' loaded'
                i = i + 1
                
    store_integrals(images, label)
    return images

def load_integral_images_faces():
    f = open('INTEGRALFACES', 'r')
    with f as input:
        images = pickle.load(input)
    return images
    
def load_integral_images_nonfaces():
    f = open('INTEGRALNONFACES', 'r')
    with f as input:
        images = pickle.load(input)
    return images
    
def store_integrals(images, label):
    if label == 1:
        f = open('INTEGRALFACES', 'w')
    else:
        f = open('INTEGRALNONFACES', 'w')
    with f as output:
        pickle.dump(images, output, pickle.HIGHEST_PROTOCOL)


def main():
    #Load faces images with label of 1
    facepath = os.path.abspath('INTEGRALFACES')
    if os.path.isfile(facepath):
        faces = load_integral_images_faces()
        print 'Loaded faces file'
    else:
        print 'Loading faces'
        faces = store_integral_images("faces/", 1)
        
    #Load nonfaces imaegs with Label of 0
    nonfacepath = os.path.abspath('INTEGRALNONFACES')
    if os.path.isfile(nonfacepath):
        nonfaces = load_integral_images_nonfaces()
        print 'Loaded nonfaces file'
    else:
        print 'Loading non-faces'
        nonfaces = store_integral_images("nonfaces/", 0)

    #Train classifiers
    hypotheses = 20
    classifiers = train(faces, nonfaces, hypotheses)
    
    #Load test images to classifiers
    testImage = faces + nonfaces
    
    for image in testImage:
        result = testImages(classifiers, image)
        if image.label == 1 and result == 1:
            correct_faces += 1
        if image.label == -1 and result == -1:
            correct_non_faces += 1
            
    print '..done. Result:\n  Faces: ' + str(correct_faces) + '/' + str(len(faces)) + '\n  non-Faces: ' + str(correct_non_faces) + '/' + str(len(non_faces))
    
if __name__ == "__main__":
    main()
