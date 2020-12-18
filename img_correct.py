# -*- coding: UTF-8 -*-
import os
import imghdr
import cv2
import numpy as np
from skimage import io
from skimage.feature import canny
from skimage.color import rgb2gray
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import rotate
from PIL import Image
from black_edges_detection import edge_detection


class SkewDetect:

    piby4 = np.pi / 4

    def __init__(
        self,
        input_file=None,
        batch_path=None,
        output_file=None,
        sigma=3.0,
        display_output=None,
        num_peaks=20,
        plot_hough=None
    ):

        self.sigma = sigma
        self.input_file = input_file
        self.batch_path = batch_path
        self.output_file = output_file
        self.display_output = display_output
        self.num_peaks = num_peaks
        self.plot_hough = plot_hough

    def write_to_file(self, wfile, data):

        for d in data:
            wfile.write(d + ': ' + str(data[d]) + '\n')
        wfile.write('\n')

    def get_max_freq_elem(self, arr):

        max_arr = []
        freqs = {}
        for i in arr:
            if i in freqs:
                freqs[i] += 1
            else:
                freqs[i] = 1

        sorted_keys = sorted(freqs, key=freqs.get, reverse=True)
        max_freq = freqs[sorted_keys[0]]

        for k in sorted_keys:
            if freqs[k] == max_freq:
                max_arr.append(k)

        return max_arr

   

    def compare_sum(self, value):
        if value >= 44 and value <= 46:
            return True
        else:
            return False

    def display(self, data):

        for i in data:
            print(i + ": " + str(data[i]))

    def calculate_deviation(self, angle):

        angle_in_degrees = np.abs(angle)
        deviation = np.abs(SkewDetect.piby4 - angle_in_degrees)

        return deviation

    def run(self):

        if self.display_output:
            if self.display_output.lower() == 'yes':
                self.display_output = True
            else:
                self.display_output = False

        if self.plot_hough:
            if self.plot_hough.lower() == 'yes':
                self.plot_hough = True
            else:
                self.plot_hough = False

        if self.input_file is None:
            if self.batch_path:
                self.batch_process()
            else:
                print("Invalid input, nothing to process.")
        else:
            self.process_single_file()

    def check_path(self, path):

        if os.path.isabs(path):
            full_path = path
        else:
            full_path = os.getcwd() + '/' + str(path)
        return full_path

    def process_single_file(self):

        file_path = self.check_path(self.input_file)
        res = self.determine_skew(file_path)
        print(res)

        if self.output_file:
            output_path = self.check_path(self.output_file)
            wfile = open(output_path, 'w')
            self.write_to_file(wfile, res)
            wfile.close()

        return res

    def batch_process(self):
        wfile = None
        file_path = self.check_path (self.input_file)
        if self.batch_path == '.':
            self.batch_path = ''

        abs_path = self.check_path(self.batch_path)
        files = os.listdir(abs_path)

        if self.output_file:
            out_path = self.check_path(self.output_file)
            wfile = open(file_path, 'w')

        for f in files:
            file_path = abs_path + '/' + f
            if os.path.isdir(file_path):
                continue
            if imghdr.what(file_path):
                res = self.determine_skew(file_path)
                if wfile:
                    self.write_to_file(wfile, res)
        if wfile:
            wfile.close()

    def determine_skew(self, img_file):
        img = io.imread(img_file, as_grey=True)
        edges = canny(img, sigma=self.sigma)
        h, a, d = hough_line(edges)
        _, ap, _ = hough_line_peaks(h, a, d, num_peaks=self.num_peaks)

        if len(ap) == 0:
            return {"Image File": img_file, "Message": "Bad Quality"}

        absolute_deviations = [self.calculate_deviation(k) for k in ap]
        average_deviation = np.mean(np.rad2deg(absolute_deviations))
        ap_deg = [np.rad2deg(x) for x in ap]

        bin_0_45 = []
        bin_45_90 = []
        bin_0_45n = []
        bin_45_90n = []

        for ang in ap_deg:

            deviation_sum = int(90 - ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_45_90.append(ang)
                continue

            deviation_sum = int(ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_0_45.append(ang)
                continue

            deviation_sum = int(-ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_0_45n.append(ang)
                continue

            deviation_sum = int(90 + ang + average_deviation)
            if self.compare_sum(deviation_sum):
                bin_45_90n.append(ang)

        angles = [bin_0_45, bin_45_90, bin_0_45n, bin_45_90n]
        lmax = 0

        for j in range(len(angles)):
            l = len(angles[j])
            if l > lmax:
                lmax = l
                maxi = j

        if lmax:
            ans_arr = self.get_max_freq_elem(angles[maxi])
            ans_res = np.mean(ans_arr)

        else:
            ans_arr = self.get_max_freq_elem(ap_deg)
            ans_res = np.mean(ans_arr)

        data = {
            "Image File": img_file,
            "Average Deviation from pi/4": average_deviation,
            "Estimated Angle": ans_res,
            "Angle bins": angles}

        if self.display_output:
            self.display(data)
  
        return data


def skew_correct(input_file):
    # input_file = r'C:\Users\28912\Desktop\insurance\xingfu\tuanxian_dianzi.jpg'
    # 定义文本旋转处理类对象
    input_file = edge_detection(input_file)
    skew_obj = SkewDetect(input_file)
    origin_img = io.imread(input_file)  # 读取图像数据
    res = skew_obj.process_single_file()
    angle = res['Estimated Angle']
    print(angle)

    if (angle >= 0) and (angle <= 90):
        rot_angle = angle - 90
    if (angle >= -45) and (angle < 0):
        rot_angle = angle - 90
    if (angle >= -90) and (angle < -45):
        rot_angle = 90 + angle

    # 根据检测出来的旋转角度进行旋转操作
    # rotated = rotate(origin_img, rot_angle, mode='wrap',preserve_range=True ) # , resize=True)`constant`, `edge`, `wrap`, `reflect` or `symmetric`.os
    # rotated = cv2.warpAffine(img, M, (cols, rows), borderValue=(255, 255, 255))
    res_path = input_file.split('.')[0] + '_res.jpg'
    # io.imsave(res_path, rotated)
   
    img = Image.open(input_file)
    im2 = img.convert('RGBA')
    rot = im2.rotate(rot_angle, expand=1)
    fff = Image.new('RGBA', rot.size, (255,)*4)
    out = Image.composite(rot, fff, rot)
    out.convert(img.mode).save(res_path)

    # cv2.putText(rotated, "angle: {:.2f} ".format(rot_angle),
        # (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.imwrite(res_path, rotated)
    
    return rot_angle, res_path

img_path = '28.jpg'
rot_angle, res_path = skew_correct(img_path)