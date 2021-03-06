"""Pattern detector
"""

import math

import cv2

from . import piv
from .geometry import Point


def _to_grayscale(image):
    """Convert given image to grayscale.
    """
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


class PatternDetector(object):
    """Find similar patterns in image1 from image2.

    Public properties:
    pattern_size -- [int, int] Pattern size
    dx_range -- [int, int] Horizontal buffer length to find
    dy_range -- [int, int] Vertical buffer length to find

    Arguments:
    image1 -- [image] Image to refer to the pattern as numpy.ndarray
    image2 -- [image] Image to find the pattern as numpy.ndarray
    """

    pattern_size = (25, 25)
    dx_range = (-5, 5)
    dy_range = (-5, 5)

    def __init__(self, image1, image2):
        self._image1 = _to_grayscale(image1)
        self._image2 = _to_grayscale(image2)

    def detect(self, point):
        """Find similar pattens in image1 from image2.

        Return:
        point -- [Point] Found point
        """
        try:
            dy, dx = piv.find_point(self._image1, self._image2, point.y,
                                    point.x, pattern_size=self.pattern_size,
                                    di_range=self.dy_range,
                                    dj_range=self.dx_range)
        except ValueError:  # frame out
            return None

        if math.isnan(dx) or math.isnan(dy):
            return None

        return Point(int(point.x + dx), int(point.y + dy))
