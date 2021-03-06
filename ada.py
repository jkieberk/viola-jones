import cv2
import numpy as np
from haar import HaarLikeFeature
from haar import FeatureTypes
from math import pow

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
                for x in range(24-width):
                    for y in range(24-height):
                        features.append(HaarLikeFeature(f, (x, y), width, height, 0, 1))
    features = np.array(features)
    print str(len(features)) + ' features created'
    
    allImages = np.concatenate([positives,negatives])
    #np.random.shuffle(allImages)
    
    classifiers = []
    # REMEMBER TO FIX!!!!!
    for t in range(T):
        denom = 0.0
        #Get denominator for normalization loop
        for image in allImages:
            #print image.weight
            denom += image.weight
        # 1. Normalize weights
        #print "denom = " + str(denom)
        for image in allImages:
            image.weight = image.weight/denom
        
        #Get total +/- weights (for use in T+ and T- later)
        totalPosWeight = 0
        totalNegWeight = 0
        for image in allImages:
            if image.label == 1:
                totalPosWeight = totalPosWeight + image.weight
            else:
                totalNegWeight = totalNegWeight + image.weight
        
        #i = 0
        imageIndex = 0
        featureIndex = -1
        #Iterate over every feature
        print "Generating " + str(len(features) * len(allImages)) + " classifiers for round " + str(t) + " (this may take a while)"
        for feature in features:
            featureIndex = featureIndex + 1
            classified = []
            for img in allImages:
                classified.append([imageIndex, feature.get_score(img)])
                imageIndex = imageIndex + 1
                #i = i + 1
                #if i % 1000000 == 0:
                    #print str(i) + " classifiers created for T " + str(t)
            imageIndex = 0        
        
            classified.sort(key=lambda x: x[1])
            
            eArray = []
            tPlus = totalPosWeight
            tMinus = totalNegWeight
            sPlus = 0
            sMinus = 0
            imgIndex = -1
            lowImgIndex = 0
            lowestE = min(tMinus, tPlus)
            
            #Find lowest threshold error at t
            for image in classified:
                imgIndex = imgIndex + 1
                #find min error threshold
                if allImages[image[0]].label == 1:
                    sPlus = sPlus + img.weight
                if allImages[image[0]].label == 0:
                    sMinus = sMinus + img.weight
                
                e = min((sPlus + (tMinus - sMinus)), (sMinus + (tPlus - sPlus)))
                eArray.append(e)
                if e < lowestE:
                    lowestE = e
                    lowImgIndex = imgIndex
            
                    
            #print "Lowest e for feature " + str(feature.type) + ": " + str(lowestE) + ", image #" + str(lowImgIndex)
            feature.threshold = (classified[lowImgIndex][1] + classified[lowImgIndex-1][1])/2
            #print "New threshold: " + str(feature.threshold)
            #featureArray.append([feature, feature.threshold])
        
        featureArray = []
        featureIndex = -1
        for feature in features:
            featureIndex = featureIndex + 1
            totalWeight = 0
            for image in allImages:
                imageLabel  = image.label
                imageVote  =  feature.get_vote(image)
                totalWeight = totalWeight + image.weight * abs(imageVote - imageLabel)
            featureArray.append([totalWeight, featureIndex])
        
        #Sort features by lowest total weight
        featureArray.sort(key=lambda x: x[0])
        
        #Get best weak classifier
        bestWeakClassifier = [featureArray[0][0], features[featureArray[0][1]]]
        #print "Lowest e = " + str(bestWeakClassifier[0])
        #del features[featureArray[1]]
        #features.delete(featureArray[1])
        features = np.delete(features, featureArray[1])
        
        beta = 0.0
        #Update weights
        correct = 0
        incorrect = 0
        for image in allImages:
            weakClassifierScore = bestWeakClassifier[1].get_vote(image)
            if(weakClassifierScore == image.label):
                correct += 1
                #If bestWeakClassifier[0] is 0 everything breaks
                beta = bestWeakClassifier[0] / (1. - bestWeakClassifier[0])
                #print "New weight = " + str(image.weight * beta)
            else:
                incorrect += 1
                score = 1
                #print bestWeakClassifier[0]
                #print 1- bestWeakClassifier[0]
                #print ''
                beta = 1.0
                #print "Weight = " + str(image.weight * beta)
            image.weight = image.weight * beta
            #print image.weight
        classifiers.append([bestWeakClassifier[1], beta])
        #raw_input("!! Enter Enter to continue...")
        print "Correct: " + str(correct)
        print "Incorrect: " + str(incorrect)
        print "Best weak classifiers selected. Next round"
    print "Done learning."
    return classifiers            
                
                
                
                
                
                
                
                
                
                