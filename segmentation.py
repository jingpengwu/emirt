import numpy as np


class Segmentation(object):
    def __init__(self, seg):
        self._seg = seg

    def relabelid(self):
        """
        relabel the segment id from 1 to N
        """
        uni = np.unique(self._seg)
        # construct index mapping
        idx_dict = {uni[i]: i for i in xrange(len(uni))}
        for i in xrange(len(self._seg)):
            self._seg[i] = idx_dict[self._seg[i]]

    @property
    def data(self):
        """"I'm the numpy array of segmentation"""
        return self._seg

    def touint16(self):
        return np.asarray(self._seg, dtype=np.uint16)
