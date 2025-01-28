# Import packages
from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

# Load the two images
img1 = cv2.imread('images/carfresh.jpg')
img2 = cv2.imread("images/cardamage.jpg")
# Resize images if necessary
img1 = cv2.resize(img1, (600,360))
img2 = cv2.resize(img2, (600,360))

img_height = img1.shape[0]

# Grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Find the difference between the two images
# Compute the mean structural similarity index between two images (similar).
(similar, diff) = compare_ssim(gray1, gray2, full=True)
# similar belongs in the interval [-1, 1] with 1 represents perfect similarity
# Perfect similarity : both images are the same (identical)
print("Level of similarity : {:.2f}".format(similar))

# Calculate difference percentage
difference_percentage = (1 - similar) * 100
print("Difference Percentage : {:.2f}%".format(difference_percentage))

# diff is in range [0,1] so we need to convert it to an 8-bit array in range [0,255]
diff = (diff*255).astype("uint8")
cv2.imshow("Difference", diff)

# Apply threshold. Apply both THRESH_BINARY_INV and THRESH_OTSU
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv2.imshow("Threshold", thresh)

# Calculate contours
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

difference_area = 0
for contour in contours:
    # Calculate bounding box around contour
    if cv2.contourArea(contour) > 5:
        x, y, w, h = cv2.boundingRect(contour)
        # Draw rectangle - bounding box on both images
        cv2.rectangle(img1, (x, y), (x+w, y+h), (0,0,255), 2)
        cv2.rectangle(img2, (x, y), (x+w, y+h), (0,0,255), 2)
        difference_area += cv2.contourArea(contour)

# Calculate total area of the image
total_area = img1.shape[0] * img1.shape[1]

# Calculate percentage difference based on contour area
difference_area_percentage = (difference_area / total_area) * 100
print("Contour-based Difference Area Percentage: {:.2f}%".format(difference_area_percentage))

# Show images with rectangles on differences
x = np.zeros((img_height,10,3), np.uint8)
result = np.hstack((img1, x, img2))
cv2.imshow("Differences", result)

cv2.waitKey(0)
cv2.destroyAllWindows()
