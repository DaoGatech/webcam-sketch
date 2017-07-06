import cv2
import numpy as np

#kernel sharpening
kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

#blur kernel
blur_kernel = np.ones((7,7), np.float32) / 49

#Current Angel of the webcam
curAngel = 0

#opening_kernel
opening_kernel = np.ones((5,5), np.uint8)

def sketch(image):
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)
    canny_edges = cv2.Canny(img_gray_blur, 10, 70)
    ret, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
    return mask

def sharpen(image):
    return cv2.filter2D(image, -1, kernel_sharpening)

def blur(image):
    return cv2.filter2D(image, -1, blur_kernel)

def rotate(image):
    global curAngel
    curAngel = (curAngel + 90) % 360
    height, width = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), curAngel, 1)
    return cv2.warpAffine(image, rotation_matrix, (width, height))

def crop(image):
    height, width = image.shape[:2]
    start_row, start_col = int(height * .15), int(width * .15)
    end_row, end_col = int(height * .75), int(width / 2)
    return image[start_row:end_row][start_col:end_col]

def removeNoise(image):
    opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, opening_kernel)
    return opening