import cv2
import numpy as numpy
import matplotlib.pyplot as plt 

def to_gray(color_image):
	gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
	return gray

def gen_sift_features(gray_image):
	sift = cv2.xfeatures2d.SIFT_create()
	# kp is the keypoints
    #
    # desc is the SIFT descriptors, they're 128-dimensional vectors
    # that we can use for our final features
    kp, desc = sift.detectAndCompute(gray_image, None)
    return kp, desc

# Displays regular color image
def show_rgb_img(image):
	return plt.imshow(cv2.cvtColor(image, cv2.CV_32S))

def show_sift_features(gray_image, color_image, keypoints):
	return plt.imshow(cv2.drawKeypoints(gray_image, keypoints, color_image.copy()))

