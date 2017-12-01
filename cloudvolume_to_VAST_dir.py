#!/usr/bin/python
"""
T Macrina
171129

Create VAST directory from CloudVolume cutout

if using 'raw'

dst_dir/
	raw/
		[section01].tif
		[section02].tif
		...
	cell_segmentation/
	psd/
	mitochondria/
	vesicle_cloud/
	cell_semantic/

Args:
	sys.argv[1]: x start
	sys.argv[2]: x stop
	sys.argv[3]: y start
	sys.argv[4]: y stop
	sys.argv[5]: z start
	sys.argv[6]: z stop
	sys.argv[7]: path to write the VAST directory
	sys.argv[8]: path to CloudVolume directory
	sys.argv[9]: path to write TIF image directory
	sys.argv[10]: if data is uint32 (0 or 1)
	**optional:
	sys.argv[11]: path to second CloudVolume directory
	sys.argv[12]: path to write second TIF image directory
	sys.argv[13]: if data is uint32 (0 or 1)

Returns:
	Direcoty setup as above

e.g.
`python cloudvolume_to_VAST_dir.py 44600 45624 27000 28024 1 129 /usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/ground_truth/vol501 gs://neuroglancer/pinky40_v11/image raw 0 gs://neuroglancer/pinky40_v11/watershed_mst_trimmed_sem_remap cell_segmentation 1`
"""

from cloudvolume_to_tif_dir import cv_to_tif
import os
import sys
from datetime import datetime

dirs = {'raw': 'raw', 
		'cell_segmentation': 'cell_segmentation', 
		'psd': 'psd', 
		'mitochondria': 'mitochondria',
		'vesicle_cloud': 'vesicle_cloud',
		'cell_semantic': 'cell_semantic'}


def mkdir(dir):
	if not os.path.exists(dir):
		print 'Creating ' + dir
		os.makedirs(dir)
	else:
		print dir + ' already exists'

def setup_VAST_dir(dir):
	# some sort of abstraction for directory names
	mkdir(dir)
	for k, d in dirs.iteritems():
		mkdir(os.path.join(dir, d))

def main():
	x_slice = slice(int(sys.argv[1]), int(sys.argv[2]))
	y_slice = slice(int(sys.argv[3]), int(sys.argv[4]))
	z_slice = slice(int(sys.argv[5]), int(sys.argv[6]))
	dir = sys.argv[7]
	cv_path = sys.argv[8]
	image_dir = os.path.join(dir, dirs[sys.argv[9]])
	uint32 = bool(int(sys.argv[10]))
	setup_VAST_dir(dir)
	cv_to_tif(cv_path, x_slice, y_slice, z_slice, image_dir, uint32)
	readme  = 'VAST directory:\n\t' + dir + '\n'
	readme += 'x_slice:\n\t' + str(x_slice) + '\n'
	readme += 'y_slice:\n\t' + str(y_slice) + '\n'
	readme += 'z_slice:\n\t' + str(z_slice) + '\n'
	readme += dirs[sys.argv[9]] + ' layer:\n\t' + cv_path + '\n'
	if len(sys.argv) > 11:
		cv_path = sys.argv[11]
		image_dir = os.path.join(dir, dirs[sys.argv[12]])
		uint32 = bool(int(sys.argv[13]))
		cv_to_tif(cv_path, x_slice, y_slice, z_slice, image_dir, uint32)
		readme += dirs[sys.argv[12]] + ' layer:\n\t' + cv_path + '\n'
	readme += 'Created by:\n\t' 
	readme += os.getenv("USER") + '\n\t'
	readme += '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + '\n'
	readme += 'Script:\n\t' + __file__ + '\n'
	with open(os.path.join(dir, 'README.md'), 'w') as file:
		file.write(readme)

if __name__ == '__main__':
	main()