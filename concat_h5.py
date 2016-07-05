#!/usr/bin/python
"""
T Macrina
160421

Make 3D stack of UInt8 HDF5 images in a directory (sorted), crop, & save as H5

Args:
	sys.argv[1]: full path to the TIF image directory
	sys.argv[2]: filename of the H5 file (placed in the TIF directory)
	sys.argv[3:7]: start x, start y, start z, end x, end y, end z

Returns:
	H5 file saved in the same directory, in z,y,x order
"""

import numpy as np
import h5py
import os
import sys

def get_image(fn, group="/img"):
	"""Open H5 image and convert to numpy ndarray of dtype
	Image stored under /img in the H5

	Currently tested for only for uint8 -> uint8

	Args:
		fn: filename (full path) of the image

	Returns:
		An ndarray of dtype
	"""
	f = h5py.File(fn, "r")
	return np.array(f[group])

def make_array_from_h5_dir(dir):
	"""Combine all TIF images in directory (sorted) into 3D ndarray

	Args:
		dir: folder path

	Returns:
		An ndarray of dtype with at least 3 dimesnions
	"""
	array = None
	files = os.listdir(dir)
	files.sort()
	for file in files:
		if file.endswith(".h5") or file.endswith(".hdf5"):
			a = get_image(os.path.join(dir, file))
			if array is None:
				array = a
			else:
				array = np.dstack((array, a))
	return array

def write_to_h5(fn, arr):
	"""Write ndarray to H5 file under group "main"
	"""
	f = h5py.File(fn, "w")
	f.create_dataset("/main", data=arr, dtype=arr.dtype)
	f.close()

def main():
	"""Make HDF5 3D matrix of TIF images in a sorted directory & cropped
	"""
	dir = os.getcwd()
	if len(sys.argv) > 1:
		dir = sys.argv[1]
	crop = slice(None), slice(None), slice(None)
	if len(sys.argv) > 6:
		crop = (slice(int(sys.argv[3]), int(sys.argv[4])),
					slice(int(sys.argv[5]), int(sys.argv[6])),
					slice(None))
	array = make_array_from_tif_dir(dir)
	array = array[crop]
	array = array.transpose((2,1,0))
	fn = os.path.split(os.getcwd())[-1] + ".h5"
	if len(sys.argv) > 2:
		fn = sys.argv[2]
	if not fn.endswith(".h5"):
		fn += ".h5"
	write_to_h5(os.path.join(dir, fn), array)

if __name__ == '__main__':
	main()