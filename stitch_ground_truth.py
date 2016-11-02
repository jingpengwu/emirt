#!/usr/bin/python
"""
T Macrina
161103

Stitch together ground truth volumes
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

layout_fn = "/usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/ground_truth/stitched_vol19-vol34/layout.csv"
# layout = [[1,1,"/usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/ground_truth/vol19"],
# 		  [1,2,"/usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/ground_truth/vol20"]]
img_size = np.array([512,512])
# http://stackoverflow.com/questions/25298592/converting-32-bit-integer-into-array-of-four-8-bit-integers-in-python
dt = np.dtype(('i4', [('bytes','u1',4)]))

def load_layout(layout_filepath):
	layout = []
	with open(layout_filepath, mode='r') as f:
		reader = csv.reader(f)
		for row in reader:
			layout.append([int(row[0]), int(row[1]), row[2]])
	return layout

def create_blank_image(locations, labels):
	dtype = np.uint8
	if labels:
		dtype = np.uint32
	indices = np.array(locations)
	max_indices = np.max(indices, 0)
	blank_shape = np.multiply(max_indices, img_size)
	return np.zeros(blank_shape, dtype)

def uint24_to_uint32(arr):
	img = np.dstack((np.zeros(arr.shape[:2]+(1,)), arr))
	img = img[:,:, ::-1]
	img = img.astype(np.uint8).view(np.uint32)
	return img.reshape(arr.shape[:2])

def uint32_to_uint24(arr):
	img = arr.view(dtype=dt)
	return img['bytes'][:,:,:3][:,:,::-1]

def crop_image(img, crop=(slice(0,img_size[0]), slice(0,img_size[1]))):
	return img[crop]

def stitch_images(images, locations, labels=False):
	o = create_blank_image(locations, labels)
	max_px = 0
	for (img, (r,c)) in zip(images, locations):
		ij = (slice((r-1)*img_size[0], r*img_size[0]), 
				slice((c-1)*img_size[1], c*img_size[1]))
		if labels:
			imgZ = img != 0
			img += max_px
			img = np.multiply(img, imgZ)
			max_px = np.max(img) + 1
		o[ij] = img
	return o

def load_images(filenames, labels):
	images = []
	for fn in filenames:
		try:
			img = np.array(imread(fn))
			if labels:
				img = uint24_to_uint32(img)
			images.append(crop_image(img))
		except:
			print "Cannot load: " + fn
			raise
	return images

def create_locations(layout):
	a = zip(*layout)
	rows = a[0]
	cols = a[1]
	return zip(rows, cols)

def create_image_list(layout, src_dir_name):
	filenames_list = []
	dirs = zip(*layout)[2]
	for d in dirs:
		src_dir = os.path.join(d, src_dir_name)
		filenames = glob.glob(src_dir + "/*.tif")
		filenames.sort()
		filenames = [os.path.join(src_dir, fn) for fn in filenames]
		filenames_list.append(filenames)
	return zip(*filenames_list)

def main():
	layout = load_layout(layout_fn)
	src_dir_name = sys.argv[1]
	if src_dir_name != 'raw':
		labels = True
	dst_dir = os.path.join(sys.argv[2], sys.argv[1])
	if not os.path.exists(dst_dir):
		os.makedirs(dst_dir)
	locations = create_locations(layout)
	image_filenames_list = create_image_list(layout, src_dir_name)
	for k, image_filenames in enumerate(image_filenames_list):
		images = load_images(image_filenames, labels)
		stitched = stitch_images(images, locations, labels)
		fn = src_dir_name + "%03d.tif" % k
		out_fn = os.path.join(dst_dir, fn)
		print 'saving ' + str(image_filenames) + "\n\t=> " + out_fn
		if labels:
			stitched = uint32_to_uint24(stitched)
		stitched = Image.fromarray(stitched)
		stitched.save(out_fn)

if __name__ == '__main__':
	main()