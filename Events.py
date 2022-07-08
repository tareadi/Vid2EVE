from math import log
import numpy as np
from tqdm import tqdm , trange
import cv2
from PIL import Image
import datatable as dtable
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
from numpy import asarray
import moviepy.editor as mpy
import os




def save_event(diff_brightness, threhold, n_max, i, j, time_gap, p):

    mod_diff = int(diff_brightness / threhold)
    evenum = None
    if mod_diff > n_max:
        evenum = n_max
    else:
        evenum = mod_diff

    for e in range(0, evenum):
        with open("events.text", 'a+', encoding='utf-8') as f:
            f.write("{} ".format(time_gap))
            f.write("{} ".format(i))
            f.write("{} ".format(j))
            f.write("{}\n".format(p))
        pass


class Event:

    def __init__(self, image_width, image_height, fixed_thres, adapt_thres_coef_shift):
        self.image_width = image_width
        self.image_height = image_height
        self.fixed_thres = fixed_thres  # 0.4
        self.adapt_thres_coef_shift = adapt_thres_coef_shift  # 0.05


    def initialize_frame(self, init_value):
        size_image = (self.image_height, self.image_width)
        if init_value == 0:
            frame = np.zeros(size_image)
        if init_value != 0:
            frame = np.full(size_image, init_value)
        return frame

    def log_frame(self, frame):
        new_frame = frame
        for i in range(0, self.image_height):
            for j in range(0, self.image_width):
                if new_frame[i][j] != 0:
                    new_frame[i][j] = log(frame[i][j])
                else:
                    new_frame[i][j] = 0.
        return new_frame

    def read_frame(self, frame):

        # luminance value
        size_image = (self.image_height, self.image_width)
        new_frame = np.zeros(size_image)
        for i in range(0, self.image_height):
            for j in range(0, self.image_width):
                new_frame[i][j] = frame[i][j][0] * 0.299 + frame[i][j][1] * 0.587 + frame[i][j][2] * 0.114
        return new_frame

    def generate_events(self, pic_file, time_stamp,):

        d = 1
        T_map = self.initialize_frame(self.fixed_thres)
        id_ = 0  # reference first input frame
        blocksize = 1  # till 3
        n_max = 1

        reference_frame = self.read_frame(pic_file[id_])
        reference_frame = self.log_frame(reference_frame)

        for id in (trange(len(pic_file))):
            input_frame = self.read_frame(pic_file[id])
            input_frame = self.log_frame(input_frame)

            for i in (range(0, self.image_height, blocksize)):
                for j in range(0, self.image_width, blocksize):
                    diff = None
                    diff_ = 0
                    i_shift = 0
                    j_shift = 0
                    ii = 0
                    while ii < blocksize:
                        jj = 0
                        while jj < blocksize:
                            diff = abs(input_frame[i + ii][j + jj] - reference_frame[i + ii][j + jj])
                            if diff > diff_:
                                diff_ = diff
                                i_shift = ii
                                j_shift = jj
                            jj += 1
                        ii += 1

                    diff_brightness = input_frame[i + i_shift][j + j_shift] - reference_frame[i + i_shift][j + j_shift]

                    # Assigning Polarities on/off --> 1/0
                    if diff_brightness > T_map[i + i_shift][j + j_shift]:
                        p = 1

                        ##save events with on polarity
                        save_event(diff_brightness, self.fixed_thres, n_max, i, j, time_stamp[id], p)

                    elif diff_brightness < -T_map[i + i_shift][j + j_shift]:
                        diff_brightness = - diff_brightness
                        p = 0

                        ##save events with off polarity
                        save_event(diff_brightness, self.fixed_thres, n_max, i, j, time_stamp[id], p)

                    else:
                        T_map[i][j] = T_map[i][j] * (1 - self.adapt_thres_coef_shift)

                    #### updating references copy for difference calculation
                    if d == 1:
                        m = 0
                        while m < blocksize:
                            n = 0
                            while n < blocksize:
                                reference_frame[i + m][j + n] = input_frame[i + m][j + n]
                                n += 1
                            m += 1

        return ("DONE Conversion! ...  ")
        pass


