# from https://github.com/Simon-Hohberg/Viola-Jones/blob/master/src/de/fu/violajones/HaarLikeFeature.py

from enum import Enum

#def enum(**enums):
#    return type('Enum', (), enums)

class FeatureType(Enum):
    TWO_VERTICAL = (1,2)
    TWO_HORIZONTAL = (2,1)
    THREE_HORIZONTAL = (3,1)
    THREE_VERTICAL = (1,3)
    FOUR = (2,2)
    
FeatureTypes = [FeatureType['TWO_VERTICAL'].value, FeatureType['TWO_HORIZONTAL'].value, FeatureType['THREE_VERTICAL'].value, FeatureType['THREE_HORIZONTAL'].value, FeatureType['FOUR'].value]
#FeatureType = enum(TWO_VERTICAL = (1,2), TWO_HORIZONTAL = (2,1), THREE_HORIZONTAL = (3,1), THREE_VERTICAL = (1,3), FOUR = (2,2))

class HaarLikeFeature(object):
    '''
    classdocs
    '''


    def __init__(self, feature_type, position, width, height, threshold, polarity):
        '''
        @param feature_type: see FeatureType enum
        @param position: top left corner where the feature begins (tuple)
        @param width: width of the feature
        @param height: height of the feature
        @param threshold: feature threshold
        @param polarity: polarity of the feature (-1, 1)
        '''
        self.type = feature_type
        self.top_left = position
        self.bottom_right = (position[0] + width, position[1] + height)
        self.width = width
        self.height = height
        self.threshold = threshold
        self.polarity = polarity
    
    def get_score(self, intImage):
        score = 0
        if self.type == FeatureType['TWO_VERTICAL'].value:
            print "two vert"
            first = intImage.integralBox(self.top_left, (self.top_left[0] + self.width, self.top_left[1] + self.height/2))
            second = intImage.integralBox(self.top_left[0], self.top_left[1] + self.height/2), self.bottom_right)
            score = first - second
        elif self.type== FeatureType['TWO_HORIZONTAL'].value:
            print "two horiz"
            first = intImage.integralBox(self.top_left, (self.top_left[0] + self.width/2, self.top_left[1] + self.height))
            second = intImage.integralBox((self.top_left[0] + self.width/2, self.top_left[1]), self.bottom_right)
            score = first - second
        elif self.type == FeatureType['THREE_HORIZONTAL'].value:
            print "three horiz"
            first = intImage.integralBox(self.top_left, (self.top_left[0] + self.width/3, self.top_left[1] + self.height))
            second = intImage.integralBox((self.top_left[0] + self.width/3, self.top_left[1]), (self.top_left[0] + 2*self.width/3, self.top_left[1] + self.height))
            third = intImage.integralBox((self.top_left[0] + 2*self.width/3, self.top_left[1]), self.bottom_right)
            score = first - second + third
        elif self.type == FeatureType['THREE_VERTICAL'].value:
            print "three horiz"
            first = intImage.integralBox(self.top_left, (self.bottom_right[0], self.top_left[1] + self.height/3))
            second = intImage.integralBox((self.top_left[0], self.top_left[1]+ self.height/3), (self.bottom_right[0], self.top_left[1] + 2*self.height/3))
            third = intImage.integralBox((self.top_left[0], self.top_left[1] + 2*self.height/3), self.bottom_right)
            score = first - second + third
        elif self.type == FeatureType['FOUR'].value:
            print "four"
            # top left area
            first = intImage.integralBox(self.top_left, (self.top_left[0] + self.width/2, self.top_left[1] + self.height/2))
            # top right area
            second = intImage.integralBox((self.top_left[0] + self.width/2, self.top_left[1]), (self.bottom_right[0], self.top_left[1] + self.height/2))
            # bottom left area
            third = intImage.integralBox((self.top_left[0], self.top_left[1] + self.height/2), (self.top_left[0] + self.width/2, self.bottom_right[1]))
            # bottom right area
            fourth = intImage.integralBox((self.top_left[0] + self.width/2, self.top_left[1] + self.height/2), self.bottom_right)
            score = first - second - third + fourth
        return score
    
    def get_vote(self, intImage):
      
        score = self.get_score(intImage)
        #print score
        return 1 if score < self.polarity*self.threshold else -1
        
#Source: https://github.com/Simon-Hohberg/Viola-Jones/blob/master/src/de/fu/violajones/HaarLikeFeature.py