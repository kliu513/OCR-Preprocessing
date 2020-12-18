import cv2
import numpy as np

def erode2dilate(img, kernel_args):
    kernel = np.ones(kernel_args, np.uint8)
    erode = cv2.erode(img, kernel)
    return cv2.dilate(erode, kernel, iterations=2)

def focus_points(img):
    white = np.argwhere(img > 0)
    for pt in white:
        row = pt[0]
        col = pt[1]
        img[row+1, col] = 0
        img[row, col+1] = 0
    return np.argwhere(img > 0), img

def split_table(positions, img, focus):
    rows = []
    for pt in positions:
        if pt[0] not in rows:
            rows.append(pt[0])
    for i in range(len(rows)-1):
        cols1 = []
        cols2 = []
        for pt in positions:
            if pt[0] == rows[i]:
                cols1.append(pt[1])
            elif pt[0] == rows[i+1]:
                cols2.append(pt[1])
        cols = list(set(cols1).intersection(set(cols2)))
        cols.sort()
        print(cols)
        for j in range(len(cols)-1):
            region = img[rows[i]:rows[i+1], cols[j]:cols[j+1]]
            cv2.imshow('region'+str(i)+str(j), region)
    """
    rows = []
    cols = []
    for pt in positions:
        if pt[0] not in rows:
            rows.append(pt[0])
        if pt[1] not in cols:
            cols.append(pt[1])
    rows.sort()
    cols.sort()
    print(rows, cols)
    for i in range((len(rows)-1)):
        for j in range((len(cols)-1)):
            if focus[rows[i], cols[j]] != 0 and focus[rows[i], cols[j+1]] != 0:
                if focus[rows[i+1], cols[j]] != 0 and focus[rows[i+1], cols[j+1]] != 0:
                    region = img[rows[i]:rows[i+1], cols[j]:cols[j+1]]
                    cv2.imshow('region'+str(i)+str(j), region)
    """

def extract_table(img):
    """
    Extract and remove tables from an image
    img: an image object
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    rows, cols=binary.shape
    scale = 10
    transverse = erode2dilate(binary, (1,cols//scale))
    vertical = erode2dilate(binary, (rows//scale,1))
    points = cv2.bitwise_and(vertical, transverse)
    positions, focus = focus_points(points)
    split_table(positions, img, focus)
    """
    cv2.imshow('binary', binary)
    cv2.imshow('vert', vertical)
    cv2.imshow('trans', transverse)
    cv2.imshow('pts', points)
    """

if __name__ == "__main__":
    img = cv2.imread('scan.png')
    extract_table(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
