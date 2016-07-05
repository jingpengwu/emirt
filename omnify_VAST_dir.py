#!/usr/bin/python
"""
T Macrina
160705

Create Omni project given VAST directory. Compile raw directory & cells 
segmentation directory for channel and segmentation files, then omnify.

Args:
	None

Returns:
	Omni project saved in the directory where the script is run
"""

import os
import sys
import shutil
import omnify
import tif_dir_to_h5 as tif2h5

def main():
	cwd = os.getcwd()
	raw = os.path.join(cwd, 'raw')
	seg = os.path.join(cwd, 'cells_segmentation')
	chann_fn = 'chann.h5'
	seg_fn = 'seg.h5'
	print 'Compiling channel data'
	tif2h5.main(raw, chann_fn)
	print 'Copying channel data'
	shutil.move(os.path.join(raw, chann_fn), os.path.join(cwd, chann_fn))
	print 'Compiling cells segmentation data'
	tif2h5.main(seg, seg_fn)
	print 'Copying cells segmentation data'
	shutil.move(os.path.join(seg, seg_fn), os.path.join(cwd, seg_fn))
	print 'Start omnification'
	omnify.main(chann_fn, seg_fn)

if __name__ == '__main__':
	main()