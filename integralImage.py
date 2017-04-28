import cv2
import numpy as np

class integralImage:
    # returns integral image as numpy 2-d array
    def __init__(self, image, label):
        self.original = np.array(image)
        self.sum = 0
        self.label = label
        self.integral()
        self.weight = 0
        
    def integral(self):
        height = self.original.shape[0]
        width  = self.original.shape[1]
        integral =  np.zeros((height,width))
        integral[0][0] = self.original[0][0]
        for i in range(1,width):
            integral[0][i] = integral[0][i-1] + self.original[0][i]
        for i in range(1,height):
            integral[i][0] = integral[i-1][0] + self.original[i][0]
        for i in range(1,height):
            for j in range(1,width):
                integral[i][j] = self.original[i][j] + integral[i-1][j] + integral[i][j-1] - integral[i-1][j-1]
        print integral
        return integral
    
    # computes integral box (x1,y1) is coord of upper left bound
    #                       (x2,y2) is coord of lower right bound
    def integralBox(self,integral, x1, y1, x2, y2):
        return integral[x1][y1] + integral[x2][y2] - integral[x1][y2] - integral[x2][y1]
    
    # Testing integral function
    # class testIntegral(object):
    #     data = [[5,2,5,2],[3,6,3,6],[5,2,5,2],[3,6,3,6]]
    
    #     def __getitem__(self, key):
    #         return self.data[key]
    #     def __init__(self):
    #         self.shape = (4,4)
