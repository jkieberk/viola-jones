import cv2
import numpy as np
from integralImage import integralImage
from ada import train
import os
import pickle

def testImages(classifiers, image):
    #c[0][0] feature, c[0][1] beta
    #print "is " + str(sum([c[0].get_vote(image) * np.log(1/c[1]) for c in classifiers])) + " >= " + str(0.5 * sum([np.log(1/c[1]) for c in classifiers])) + "?"
    return 1 if sum([c[0].get_vote(image) * np.log(1/c[1]) for c in classifiers]) >= 0.5 * sum([np.log(1/c[1]) for c in classifiers]) else 0

def load_test_images(path, label):
    images = []
    i = 1
    for _file in os.listdir(path):
        if _file.endswith('.jpg'):
            if i < 50:
                images.append(integralImage(os.path.join(path, _file), label))
                i = i + 1
    return images   
    
def main():
    
    print "Loading classifiers"
    f = open('CLASSIFIERS', 'r')
    with f as input:
        classifiers = pickle.load(input)
    
    g = 1
    for c in classifiers:
        print "Feature " + str(g)
        print "Type      : " + str(c[0].type)
        print "Top left  : " + str(c[0].top_left)
        print "Width     : " + str(c[0].width)
        print "Height    : " + str(c[0].height)
        print "Threshold : " + str(c[0].threshold)
        g += 1
        
    print "Loading test images"
    #Load test images to classifiers
    testfaces = load_test_images("faces/", 1)
    testnonfaces = load_test_images("nonfaces/", 0)
    
    testImage = testfaces + testnonfaces
    
    correct_faces = 0
    correct_non_faces = 0
    for image in testImage:
        result = testImages(classifiers, image)
        if image.label == 1 and result == 1:
            correct_faces += 1
        if image.label == 0 and result == 0:
            correct_non_faces += 1
            
    print 'Result:\n  Faces: ' + str(correct_faces) + '/' + str(len(testfaces)) + '\n  non-Faces: ' + str(correct_non_faces) + '/' + str(len(testnonfaces))


if __name__ == "__main__":
    main()
