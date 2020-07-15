# lane_detection.py

import cv2
import numpy as np
import time, datetime, os
import math

width = 960
height = 540

cv2.namedWindow('LANE DETECTION', cv2.WINDOW_NORMAL)
cv2.namedWindow('ORIGINAL LANE', cv2.WINDOW_NORMAL)
cv2.namedWindow('ROI IMAGE', cv2.WINDOW_NORMAL)

lane_original = cv2.imread('../samples/lane_example.jpeg')

lane_black = cv2.cvtColor(lane_original, cv2.COLOR_BGR2GRAY)
lane_image_sample = cv2.Canny(lane_black, threshold1=100, threshold2=175)

length = 0
width = 0

# roi values (4 points)
point_1 = [110, height - 1]
point_2 = [320, 340]
point_3 = [600, 340]
point_4 = [930, height - 1]

set_points = [point_1, point_2, point_3, point_4]

# adjust to region of interest
def region_of_interest(image):
    vertices = np.array(set_points, dtype=np.int32)

    # create mask to image dimensions
    mask = np.zeros_like(image)
    
    # fill the mask (black)
    cv2.fillPoly(mask, [vertices], 255)
    
    # only show area that is the mask
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# width_threshold for lane detection
def width_threshold(row):
    threshold_seperated_min = 7
    threshold_seperated_max = 20
    threshold_continuous_min = None
    threshold_continuous_max = None

    indexes = []
    
    for i in row[point_1[0] : point_4[0]]:
        if i == 255:
            if len(indexes) == 0:
                    indexes.append(i + point_1[0])
            else:
                if (i + point_1[0]) - indexes[0] < threshold_seperated_max and\
                   (i + point_1[0]) - indexes[0] > threshold_seperated_min:
                    indexes.append(i + point_0[0])
                else:
                    indexes.clear()
                
    if len(indexes) > 0:
        print(indexes)
    indexes.clear()
    pass

print("Sample shape:", lane_image_sample.shape)

# get image adjusted to region of interest
adjusted_image = region_of_interest(lane_image_sample)

# run width thresholds to get lanes
for row in adjusted_image:
    width_threshold(row[point_1[1]:])

cv2.imshow('ORIGINAL LANE', lane_original)
cv2.imshow('LANE DETECTION', lane_image_sample)
cv2.imshow('ROI IMAGE', adjusted_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
