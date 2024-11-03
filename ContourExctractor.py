import os
import time
from multiprocessing.pool import ThreadPool
from queue import Queue

import cv2
import imutils
import numpy as np

from Application.Config import Config
from Application.VideoReader import VideoReader

class ContourExtractor:
    def __init__(self, config):
        self.frame_buffer = Queue(16)
        self.extracted_contours = dict()
        self.extracted_masks = dict()
        self.min_area = config["min_area"]
        self.max_area = config["max_area"]
        self.threshold = config["threshold"]
        self.resize_width = config["resizeWidth"]
        self.video_path = config["inputPath"]
        self.x_dim = 0
        self.y_dim = 0
        self.config = config
        self.last_frames = None
        self.averages = dict()

        print("ContourExtractor initiated")

    def get_extracted_contours(self):
        return self.extracted_contours

    def get_extracted_masks(self):
        return self.extracted_masks

    def extract_contours(self):
        self.start = time.time()
        with VideoReader(self.config) as videoReader:
            self.fps = videoReader.get_fps()
            self.length = videoReader.get_length()

            with ThreadPool(os.cpu_count()) as pool:
                while True:
                    while not videoReader.video_ended() and videoReader.buffer.qsize() == 0:
                        time.sleep(0.5)

                    tmp_data = [videoReader.pop() for _ in range(videoReader.buffer.qsize())]
                    if videoReader.video_ended():
                        break
                    pool.map(self.compute_moving_average, (tmp_data,))
                    pool.map(self.get_contours, tmp_data)

        return self.extracted_contours, self.extracted_masks

    def get_contours(self, data):
        frame_count, frame = data
        # wait for the reference frame, which is calculated by averaging some previous frames
        while frame_count not in self.averages:
            time.sleep(0.1)
        first_frame = self.averages.pop(frame_count, None)

        if frame_count % (10 * self.fps) == 1:
            print(
                f" \r \033[K {round((frame_count/self.fps)*100/self.length, 2)} % processed in {round(time.time() - self.start, 2)}s",
                end="\r",
            )

        gray = self.prepare_frame(frame)
        frame_delta = cv2.absdiff(gray, first_frame)
        thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=10)

        # Find contours of the moving objects
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        filtered_contours = []
        masks = []
        for contour in contours:
            if cv2.contourArea(contour) < self.min_area or cv2.contourArea(contour) > self.max_area:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            filtered_contours.append((x, y, w, h))
            masks.append(np.packbits(np.copy(thresh[y: y + h, x: x + w]), axis=0))

        if filtered_contours:
            self.extracted_contours[frame_count] = filtered_contours
            self.extracted_masks[frame_count] = masks

    def prepare_frame(self, frame):
        frame = imutils.resize(frame, width=self.resize_width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        return gray

    def compute_moving_average(self, frames):
        average_frames = self.config["avgNum"]

        if frames[0][0] < average_frames:
            frame = frames[0][1]
            frame = self.prepare_frame(frame)
            for j in range(len(frames)):
                frame_number, _ = frames[j]
                self.averages[frame_number] = frame
            self.last_frames = frames[-average_frames:]
            return

        if self.last_frames is not None:
            frames = self.last_frames + frames

        tmp = [[j, frames, average_frames] for j in range(average_frames, len(frames))]
        with ThreadPool(os.cpu_count()) as pool:
            pool.map(self.average_da_frames, tmp)

        self.last_frames = frames[-average_frames:]

    def average_da_frames(self, dat):
        j, frames, average_frames = dat
        frame_number, frame = frames[j]
        frame = self.prepare_frame(frame)

        avg = frame / average_frames
        for jj in range(average_frames - 1):
            avg += self.prepare_frame(frames[j - jj][1]) / average_frames
        self.averages[frame_number] = np.array(np.round(avg), dtype=np.uint8)
