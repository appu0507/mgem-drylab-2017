import cv2
from PIL import Image, ImageChops, ImageEnhance
import numpy as np

#import image
im_original = Image.open("May26 1.tif")
im_background = Image.open("May26 3.tif")

#subtract the background from the original
im_diff = ImageChops.subtract(im_original, im_background)

#enhances contrast of image
enhancer = ImageEnhance.Contrast(im_diff)
im_diff = enhancer.enhance(2.0)

#enhance brightness of image
enhancer = ImageEnhance.Brightness(im_diff)
im_diff = enhancer.enhance(2.0)

#save new image
im_diff.save ("difference.jpg")


#BROKEN OLD CODE
# #import image to numpy array
# im_original = cv2.imread("May26 3.tif")
# im_background = cv2.imread("May26 1.tif")
# 
# #matrix subtraction
# diff_BGR = np.subtract(im_original, im_background)
# #since open_cv reads image in BGR, we must convert it back to RGB using this line below
# diff_RGB = cv2.cvtColor(diff_BGR, cv2.COLOR_BGR2RGB)
# 
# #save the difference numpy array as an image
# im_diff = Image.fromarray(diff_RGB)
# im_diff.save("difference.tif")