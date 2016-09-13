#!/usr/bin/python
"""
T Macrina
160321

Crop all TIFs in a directory and save as renamed TIFs in the directory

Args:
	sys.argv[1]: full path to the TIF image directory
	sys.argv[2:6]: x slice start, x slice end, y slice start, y slice end

Returns:
	Renamed cropped TIFs
"""

# from PIL import Image
from scipy.misc import imread
from scipy.misc import imsave
import numpy as np
import h5py
import os
import sys

def convert_to_uint32(arr):
	n = 4 - arr.shape[2]
	return np.dstack((arr, np.zeros(arr.shape[:2]+(n,)))).astype(np.uint8)

def tif_to_array(fn):
	"""Open TIF image and convert to numpy ndarray of dtype

	Args:
		fn: filename (full path) of the image

	Returns:
		An ndarray of dtype
	"""
	arr = np.array(imread(fn))
	return arr

def crop_dir(src_dir, dst_dir, crop, use_uint32=False):
	"""Combine all TIF images in directory (sorted) into 3D ndarray

	Args:
		dir: folder path

	Returns:
		An ndarray of dtype with at least 3 dimesnions
	"""
	array = None
	files = os.listdir(src_dir)
	files.sort()
	for file in files:
		if file.endswith(".tif") or file.endswith(".tiff"):
			src_fn = os.path.join(src_dir, file)
			arr = tif_to_array(src_fn)
			c = crop
			if len(arr.shape) > 2:
				c = crop + (slice(None),)
			dst_fn = os.path.join(dst_dir, file)
			arr = arr[c]
			if use_uint32:
				arr = convert_to_uint32(arr)
			write_to_tif(dst_fn, arr)

def write_to_tif(fn, arr):
	"""Write ndarray to tif file
	"""
	imsave(fn, arr)

def main():
	"""Make HDF5 3D matrix of TIF images in a sorted directory & cropped
	"""
	src_dir = sys.argv[1]
	dst_dir = sys.argv[2]
	crop = (slice(int(sys.argv[3]), int(sys.argv[4])),
				slice(int(sys.argv[5]), int(sys.argv[6])))
	use_uint32 = int(sys.argv[7]) == 1
	crop_dir(src_dir, dst_dir, crop, use_uint32)
	# array = make_array_from_tif_dir(dir)
	# array = array[crop]
	# array = array.transpose((2,1,0))

if __name__ == '__main__':
	main()