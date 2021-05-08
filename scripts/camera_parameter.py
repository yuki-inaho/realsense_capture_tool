import numpy as np


class Intrinsic:
    def __init__(self):
        self.fx = None
        self.fy = None
        self.cx = None
        self.cy = None

    def set_intrinsic_parameter(self, fx, fy, cx, cy):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy

    @property
    def K(self):
        return np.array([[self.fx, 0.0, self.cx], [0.0, self.fy, self.cy], [0.0, 0.0, 1.0]])

    @property
    def center(self):
        return self.cx, self.cy

    @property
    def focal(self):
        return self.fx, self.fy