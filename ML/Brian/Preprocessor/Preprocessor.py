import os
from . import sift

class Preprocessor:
	images = []			# Pathnames to images to be processed and analyzed
	features = []		# 2D list of features for the images--length is equal to the length of the "images" list length

	def __init__(self, pathname):
		self.images = os.listdir(pathname)