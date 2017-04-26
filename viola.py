import cv2
import numpy as np
from integralImage import integralImage

def main():
    #begin viola
    img = cv2.imread("faces/BioID_0000.jpg", 0)
    ii = integralImage(img, 1)
    
    # cv2.imshow('image',img)
    

if __name__ == "__main__":
    main()