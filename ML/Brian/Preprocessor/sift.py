import cv2
import numpy as numpy
import matplotlib.pyplot as plt
import pylab

def to_gray(color_image):
	gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
	return gray

def gen_sift_features(gray_image):
	sift = cv2.xfeatures2d.SIFT_create()

	# kp is the list of keypoints
	# desc is the list of SIFT descriptors
	kp, desc = sift.detectAndCompute(gray_image, None)
	return kp, desc

# Displays regular color image
def show_rgb_img(image):
	return plt.imshow(cv2.cvtColor(image, cv2.CV_32S))

def show_sift_features(gray_image, color_image, keypoints):
	return plt.imshow(cv2.drawKeypoints(gray_image, keypoints, color_image.copy()))

#########################################################################
#	TESTING CODE
image_path = 'C:\Users\Brian\Documents\School\Capstone\goldfish.jpg'
goldfish = cv2.imread(image_path)
gray_goldfish = to_gray(goldfish)
k, d = gen_sift_features(gray_goldfish)
show_sift_features(gray_goldfish, goldfish, k)

# for i in range(0, 128):
# 	string = ''
# 	for j in range(10, 20):
# 		string += str(d[j][i]) + '\t'
# 	print string
# 	string = ''
print len(k)
pylab.show()

#########################################################################

