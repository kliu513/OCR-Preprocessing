import cv2
import numpy as np

def cam_img(img_path):
    """
    extract and remove stamps from an image
    img_path: path to an image
    """
    src = cv2.imread(img_path)
    hsv_img = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    # cv2.imshow('hsv_img', hsv_img)
    lower = np.array([0, 30, 30])
    upper = np.array([10, 255, 255])
    in_range = cv2.inRange(hsv_img, lower, upper)
    stamp = np.zeros(src.shape, np.uint8)
    stamp[:, :] = (255, 255, 255)
    stamp[in_range == 255] = src[in_range == 255]
    cv2.imwrite('stamp1.jpg', stamp)

def scan_img(img_path):
    # a substitute that deals with stacked stamps
    src = cv2.imread(img_path)
    hsv_img = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    lower1 = np.array([0, 160, 160])
    upper1 = np.array([10, 255, 255])
    in_range1 = cv2.inRange(hsv_img, lower1, upper1)
    lower2 = np.array([150, 0, 0])
    upper2 = np.array([180, 255, 255])
    in_range2 = cv2.inRange(hsv_img, lower2, upper2)
    stamp = np.zeros(src.shape, np.uint8)
    stamp[:, :] = (255, 255, 255)
    stamp[in_range1 == 255] = src[in_range1 == 255]
    stamp[in_range2 == 255] = src[in_range2 == 255]
    cv2.imwrite('stamp.jpg', stamp)

if __name__ == "__main__":
    #scan_img('scan.png')
    cam_img('cam.jpg')
