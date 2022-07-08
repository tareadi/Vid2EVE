from numpy import asarray
import cv2
from PIL import Image
import os
import moviepy.editor as mpy

def all_media_detail(path):

    frames_file = []
    time_stamp = []


    vid = mpy.VideoFileClip(path)
    count = 0
    for i, (tstamp, frame) in enumerate(vid.iter_frames(with_times=True)):
        cv2.imwrite("/Users/adityatare/Vid2EVE/frames/frame{}.jpg".format(count), frame)
        count += 1
        time_stamp.append(tstamp)

    #### extracting image width and height
    imps = Image.open("/Users/adityatare/Vid2EVE/frames/frame0.jpg")
    pix = asarray(imps)
    image_height, image_width, _ = pix.shape

    folder_dir = "/Users/adityatare/Vid2EVE/frames"
    for i in os.listdir(folder_dir):
        image = Image.open("/Users/adityatare/Vid2EVE/frames/{}".format(i))
        pix = asarray(image)
        new = pix.copy()
        frames_file.append(new)

    return frames_file, time_stamp, image_width, image_height