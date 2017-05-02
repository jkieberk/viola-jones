import cv2
import numpy as np
from haar import HaarLikeFeature
from haar import FeatureTypes

#class ada(object):
#    def __init__(self, params):

def train(positives, negatives, T):
    positives = np.asarray(positives)
    negatives = np.asarray(negatives)

    # 0. Initialize weights
    posWeight = 1./(2*len(positives))
    negWeight = 1./(2*len(negatives))
    
    for posImage in positives:
        posImage.weight = posWeight
        #print posImage.weight
    for negImage in negatives:
        #print negImage.weight
        negImage.weight = negWeight
    
    print 'Creating haar like features'
    features = []
    for f in FeatureTypes:
        for width in range(f[0],25,f[0]):
            for height in range(f[1],25,f[1]):
                for x in range(25-width):
                    for y in range(25-height):
                        features.append(HaarLikeFeature(f, (x, y), width, height, 0, 1))
    features = np.array(features)
    print str(len(features)) + ' features created'
    
    allImages = np.concatenate([positives,negatives])

    #Get denominator for normalization loop
    denom  = 0
    for image in allImages:
        denom += image.weight

    for t in range(T):
        # 1. Normalize weights
        for image in allImages:
            image.weight = image.weight/denom
        
        #2.  Select best weak classifier
        #2.1 
        classifiers = []
        for feature in features:
            for img in allImages:
                classifiers.append(feature.get_vote(img))
                
        
                