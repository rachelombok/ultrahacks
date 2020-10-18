from matplotlib import pyplot as plt
import numpy as np
import cv2
from skimage.measure import _structural_similarity as ssim

class ComparableImages:
	# Input image names to be read
	def __init__(self, file):
		#width = int(file.shape[1])
		#height = int(file.shape[0])
		image = cv2.imread(file)
		dimension = (500, 500)
		image = cv2.resize(image, dimension)
		self.image = image
		self.image_gray =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		self.image_rgb =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim.compare_ssim(imageA, imageB)
	return {'mse':m, 'ssim':s}