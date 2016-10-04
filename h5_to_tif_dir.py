#!/usr/bin/python
"""
T Macrina
160314

Make TIF images of all H5 files in directory
**H5 file must have "img" group with the image

Args:
	sys.argv[1]: full path to the H5 image directory

Returns:
	TIF files (extension changed to .tif) saved in the same directory
"""

from PIL import Image
import numpy as np
import h5py
import os
import sys

def h5_to_array(fn):
	"""Open H5 file with "img" group & convert to numpy ndarray of dtype

	Args:
		fn: filename (full path) of the image

	Returns:
		An ndarray of dtype
	"""
	f = h5py.File(fn, "r")
	if "/img" in f:
		return np.array(f["/img"]).T
	else:
		return np.array(f["/main"]).T

def write_array_to_sections(fn, arr):
	"""Split 3d ndarray along z dim into 2d sections & save as tifs
	"""
	for i in range(arr.shape[2]):
		section = arr[:,:,i]
		new_fn = os.path.splitext(fn)[0] + "_%03d.tif" % (i+1)
		write_to_tif(new_fn, section)

def write_to_tif(fn, arr):
	"""Write ndarray to tif file
	"""
	if arr.dtype == 'uint32':
		img = Image.fromarray(arr, mode='I')
	else:
		img = Image.fromarray(arr)
	img.save(fn)

def h52tif(h5_path, dir):
	"""Write directory of TIF images for each layer in 3D image H5 file
	"""
	if os.path.isfile(h5_path):
		fn = os.path.join(dir, os.path.split(h5_path)[1])
		if fn.endswith(".h5") or fn.endswith(".hdf5"):
			arr = h5_to_array(h5_path)
			write_array_to_sections(fn, arr)
	else:
		print fn + " does not exist"

def main():
	if len(sys.argv) == 2:
		fn = sys.argv[1]
		dir = os.getcwd()
		h52tif(fn, dir)
	elif len(sys.argv) == 3:
		fn = sys.argv[1]
		dir = sys.argv[2]
		h52tif(fn, dir)
	else:
		print "Need only H5 file & (optional) destination dir"

if __name__ == '__main__':
	main()
