"""Movie module for atamaTracker
"""

import cv2


class Movie(object):
    """Movie file object.

    Public properties:
    fps (read-only) -- [float] frames per second
    width (read-only) -- [int] frame dimension
    height (read-only) -- [int] frame dimension
    """

    def __init__(self, file_path):
        capture = cv2.VideoCapture(file_path)

        self.__capture = capture
        self.__fps = capture.get(cv2.cv.CV_CAP_PROP_FPS)
        self.__width = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        self.__height = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

    def __del__(self):
        self.__capture.release()

    @property
    def fps(self):
        """frames per second
        """
        return self.__fps

    @property
    def width(self):
        """frame dimension
        """
        return self.__width

    @property
    def height(self):
        """frame dimension
        """
        return self.__height

    def load_image(self, time_sec):
        """Load image at the desired time.

        Retruns None if no image could load.
        """
        self.__capture.set(cv2.cv.CV_CAP_PROP_POS_MSEC, time_sec * 1000)
        f, image = self.__capture.read()

        return image
