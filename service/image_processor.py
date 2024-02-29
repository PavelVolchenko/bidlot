import cv2
import numpy as np


class ImageProcessor:
    def __init__(self, image_data):
        self.image = cv2.cvtColor(np.array(image_data), cv2.COLOR_RGB2BGR)
        self.cropped_images = None
        self.coordinates = None
        self.filtered_image = None
        self.detected_items = None
        self.start()

    def start(self):
        self.apply_filter()
        self.find_contours()
        self.sort_contours()
        self.nparray_images_for_pillow()

    def apply_filter(self):
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        ret1, thresh = cv2.threshold(hsv, 127, 255, cv2.THRESH_TOZERO)
        canny = cv2.Canny(thresh, 700, 100, L2gradient=False)
        self.filtered_image = cv2.dilate(
            canny,
            np.ones((3, 3), dtype=int),
            iterations=2)

    def find_contours(self):
        items_contour = list()
        contours, hierarchy = cv2.findContours(
            self.filtered_image,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        min_area = 50_000
        for contour in contours:
            area = cv2.contourArea(contour)
            items_contour.append(contour) if area > min_area else None
        self.detected_items = items_contour

    def sort_contours(self):
        self.coordinates = [cv2.boundingRect(item) for item
                            in self.detected_items]
        self.coordinates.sort(key=lambda x: sum(x))

    def nparray_images(self):
        nparray_list = list()
        for coordinates in self.coordinates:
            nparray = self.crop_image(coordinates)
            nparray_list.append(nparray)
        self.cropped_images = nparray_list

    def nparray_images_for_pillow(self):
        nparray_list = list()
        for coordinates in self.coordinates:
            nparray = self.crop_image(coordinates)
            image = cv2.cvtColor(nparray, cv2.COLOR_RGB2BGR)
            nparray_list.append(image)
        self.cropped_images = nparray_list

    def crop_image(self, coordinates):
        px = 10
        x, y, w, h = coordinates
        if x - px < 0 and y - px < 0:
            x = 0
            y = 0
        else:
            x -= px
            y -= px
        return self.image[y:y + h + px * 2, x:x + w + px * 2]
