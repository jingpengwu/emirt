#!/usr/bin/python
"""
T Macrina
171129

Produce directory of TIF images, one per slice, from CloudVolume cutout

Args:
	sys.argv[1]: path to CloudVolume directory
	sys.argv[2]: x start
	sys.argv[3]: x stop
	sys.argv[4]: y start
	sys.argv[5]: y stop
	sys.argv[6]: z start
	sys.argv[7]: z stop
	sys.argv[8]: path to write TIF image directory
	sys.argv[9]: data is uint32 (0 or 1)

Returns:
	TIF files (extension changed to .tif) saved in the TIF image directory
"""

from cloudvolume import CloudVolume
from PIL import Image
import numpy as np
import sys
import os

def get_cv_cutout(path, x_slice, y_slice, z_slice):
	vol = CloudVolume(path)
	return vol[x_slice, y_slice, z_slice]

def write_uint8_to_tif(dir, arr):
	"""Split 3d ndarray along z dim into 2d sections & save as tifs
	"""
	for k in range(arr.shape[2]):
		fn = os.path.join(dir, '{:03d}.tif'.format(k+1))
		print('Writing {0}'.format(fn))
		img = Image.fromarray(arr[:,:,k].T)
		img.save(fn)

def write_rgb_to_tif(dir, arr, remap):
	"""Split 3d ndarray along z dim into 2d sections & save as tifs
	"""
	o = np.zeros(np.append(np.array(arr.shape[:-1]), 3), dtype='uint8')
	for k in range(arr.shape[2]):
		fn = os.path.join(dir, '{:03d}.tif'.format(k+1))
		print('Writing {0}'.format(fn))
		for i in range(o.shape[0]):
			for j in range(o.shape[1]):
				r,g,b = remap[arr[i,j,k]]
				o[i,j,0] = r
				o[i,j,1] = g
				o[i,j,2] = b
		img = Image.fromarray(np.transpose(o, (1,0,2)), 'RGB')
		img.save(fn)		

def cv_to_tif(cv_path, x_slice, y_slice, z_slice, dir, uint32=False):
	"""Write directory of TIF images for each layer in CV cutout
	"""
	print('Loading {0},{1},{2} from {3} to {4}, uint32: {5}'.format(x_slice, 
						y_slice, z_slice, cv_path, dir, uint32))
	arr = get_cv_cutout(cv_path, x_slice, y_slice, z_slice)[:,:,:,0]
	if uint32:
		remap = get_rgb_remap(arr)
		write_rgb_to_tif(dir, arr, remap)
	else:
		write_uint8_to_tif(dir, arr)

def get_rgb_remap(arr):
	print('Generating uint32 to rgb ID remapping')
	ids = np.unique(arr)
	remap = {}
	for k, i in enumerate(ids):
		r = np.uint8(k / 2**16)
		g = np.uint8(np.remainder(k, 2**16) / 2**8)
		b = np.uint8(np.remainder(k, 2**8))
		remap[i] = (r,g,b)
	return remap

def main():
	cv_path = sys.argv[1]
	x_slice = slice(int(sys.argv[2]), int(sys.argv[3]))
	y_slice = slice(int(sys.argv[4]), int(sys.argv[5]))
	z_slice = slice(int(sys.argv[6]), int(sys.argv[7]))
	dir = sys.argv[8]
	uint32 = bool(sys.argv[9])
	cv_to_tif(cv_path, x_slice, y_slice, z_slice, dir, uint32)

if __name__ == '__main__':
	main()
