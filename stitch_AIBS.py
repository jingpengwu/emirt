#!/usr/bin/python
"""
T Macrina
161128
Stitch together AIBS split aligned images

One section is divided into 1024x1024 chunks
Those chunks are split into folders by rows

There is a folder '0' in the root directory

Hard-coded for 512x512x100 sized volumes
Args:
	Folder_name (e.g. 'cell_segmentation', 'raw', 'psd')
	Destination directory
Returns:
	Directories with stack as stitched TIF images
"""

from PIL import Image
from scipy.misc import imread
import numpy as np
import h5py
import os
import sys
import csv
import glob

def build_fn_grid(src_dir):
	rows = glob.glob(src_dir + "/*")
	row_nums = filenames_to_nums(filenames)
	max_row = np.max(row_nums) + 1
	cols = np.array('')
	for n in row_nums:
		fn = glob.glob(src_dir + "/" + str(n) + "/*.png")
		

def filenames_to_nums(filenames):
	d = np.core.defchararray.split(filenames, '/')
	for i in range(d.shape[0]):
    	d[i] = int(d[i][-1])
    d.astype(int)
    return d