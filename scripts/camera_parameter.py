import math
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
        return np.array([
            [self.fx, 0., self.cx],
            [0., self.fy, self.cy],
            [0., 0., 1.]
        ])

    @property
    def center(self):
        return self.cx, self.cy

    @property
    def focal(self):
        return self.fx, self.fy

class Extrinsic:
    def __init__(self, translation_xyz_d2c=None, rotaion_xyz_d2c=None):
        if (translation_xyz_d2c is not None) and (rotation_xyz_d2c is not None):
            r = Rot.from_euler('xyz', rotaion_xyz_d2c, degrees=True)
            self._rotation_dcm = r.as_dcm()
            self._translation = np.array(translation_xyz_d2c)
        else:
            self._rotation_dcm = np.eye(3)
            self._translation = np.repeat(0,3)

    def set_extrinsic_parameter(self, _rotation_dcm, _translation):
        self._rotation_dcm = _rotation_dcm
        self._translation = _translation

    @property
    def rotation_dcm(self):
        return self._rotation_dcm

    @property
    def translation(self):
        return self._translation

    @property
    def transform_mat(self):
        _T = np.zeros([4,4])
        _T[:3, :3] = self._rotation_dcm
        _T[:3, 3] = self._translation
        return _T