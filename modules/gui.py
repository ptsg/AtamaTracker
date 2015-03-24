"""GUI frontend for atamaTracker
"""

import cv2
import numpy


class EventListener(object):
    """Listener for mouse events

    Public properties:
    xx -- numpy array for horizontal positions
    yy -- numpy array for vertical positions
    """
    
    def __init__(self):
        self.xx = numpy.array([], dtype=numpy.int)
        self.yy = numpy.array([], dtype=numpy.int)

    def get_xy(self, window_name):
        """Listen mouse event and return clicked coordinates.
        """
        cv2.setMouseCallback(window_name, self.__onMouseClick)
        cv2.waitKey(0)

        return self.xx, self.yy

    def __onMouseClick(self, event, x, y, flags, param):
        """Mouse event callback.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.xx = numpy.append(self.xx, x)
            self.yy = numpy.append(self.yy, y)