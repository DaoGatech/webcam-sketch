import cv2
import numpy as np

#kernel sharpening
kernel_sharpening = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])

#blur kernel
blur_kernel = np.ones((7,7), np.float32) / 49

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
