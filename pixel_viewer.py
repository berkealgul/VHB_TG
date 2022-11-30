import cv2
import numpy as np

"""
Author: Berke A.   4.10.2021  Updated : 28.11.2022
This is a tool for viewing pixel values and coordinates in video.
you can hover mouse around desired location and gather information from terminal
press a to exit application, b to pause/resume video
"""

img_ = cv2.imread("resources/full_lung_wb.png",cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img_,cv2.COLOR_BGR2BGRA) 

pixel = np.zeros((150, 150, 3), np.uint8)
pixel[:] = (10, 10, 10)

def mouse_callback(event, x, y, flags, param):
	# grab references to the global variables
    global imga
    b, g, r, aa = img[y,x,:]
    pixel[:] = (b, g, r)
    print("x:", x, " y:", y, " --  r:", r, " g:", g, " b:", b)


cap = cv2.VideoCapture()
cap.open("video.mp4") # change input if you want


cv2.namedWindow("lol")
cv2.setMouseCallback("lol", mouse_callback)

while True:
    # you can resize by half if image dosent fit your monitor
    #width = int(img.shape[1] / 2)
    #height = int(img.shape[0] / 2)
    #dim = (width, height)
    #img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow("lol", img)
    cv2.imshow("pixel", pixel)

    key = cv2.waitKey(5) 

    if key == ord('a') or key == ord('A'):
        break