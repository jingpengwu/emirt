#!/usr/bin/python
"""
T Macrina
160630

Create VAST directory to conform to the following layout

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
	[H5_channel].h5

Args:
	sys.argv[1]: full path to the H5 image (**with 'img' or 'main'  group)
	sys.argv[2]: path to the directory that should be setup as dst_dir above

Returns:
	Direcoty setup as above
"""

import os
import sys
from shutil import copyfile
from datetime import datetime
import h5_to_tif_dir as h52tif

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

def split_h5(h5_file, dir):
	if os.path.isfile(h5_file):
		fn = os.path.split(h5_file)[1]
		print 'Copying ' + fn + ' to ' + dir
		copyfile(h5_file, os.path.join(dir, fn))
		h52tif.h52tif(h5_file, os.path.join(dir, dirs['raw']))
	else:
		print h5_file + ' does not exist'

def main():
	if len(sys.argv) > 2:
		fn = sys.argv[1]
		dir = sys.argv[2]
		setup_VAST_dir(dir)
		split_h5(fn, dir)
		readme = 'VAST directory:\n\t' + dir + '\n'
		readme += 'Original H5 src:\n\t' + fn + '\n'
		readme += 'Created by:\n\t' 
		readme += os.getenv("USER") + '\n\t'
		readme += '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()) + '\n'
		readme += 'Script:\n\t' + __file__ + '\n'
		with open(os.path.join(dir, 'README.md'), 'w') as file:
			file.write(readme)
	else:
		print 'Need only H5 file & (optional) destination dir'

if __name__ == '__main__':
	main()
