import cv2
import numpy as np

# returns integral image as numpy 2-d array
def integral(img):
    height = img.shape[0]
    width  = img.shape[1]
    integral =  np.zeros((height,width))
    integral[0][0] = img[0][0]
    for i in range(1,width):
        integral[0][i] = integral[0][i-1] + img[0][i]
    for i in range(1,height):
        integral[i][0] = integral[i-1][0] + img[i][0]
    for i in range(1,height):
        for j in range(1,width):
            integral[i][j] = img[i][j] + integral[i-1][j] + integral[i][j-1] - integral[i-1][j-1]
    print integral
    return integral

# computes integral box (x1,y1) is coord of upper left bound
#                       (x2,y2) is coord of lower right bound
def integralBox(integral, x1, y1, x2, y2):
    return integral[x1][y1] + integral[x2][y2] - integral[x1][y2] - integral[x2][y1]

# Testing integral function
# class testIntegral(object):
#     data = [[5,2,5,2],[3,6,3,6],[5,2,5,2],[3,6,3,6]]

#     def __getitem__(self, key):
#         return self.data[key]
#     def __init__(self):
#         self.shape = (4,4)


def main():
    #img = cv2.imread("faces/BioID_0000.jpg", 0)
    img = testIntegral()
    integral(img)
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
