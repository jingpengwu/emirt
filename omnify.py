#!/usr/bin/python
"""
T Macrina
160701

Create Omni project given channel data & segmentation data

Args:
	sys.argv[1]: path to the channel data (H5 file data under /main)
	sys.argv[2]: path to the segmentation data (H5 file data under /main)

Returns:
	Omni project saved in the directory where the script is run
"""

import os
import sys
import shutil

def write_cmd_file(omni_fn, chann_fn, seg_fn):
	cmd = 'create:' + omni_fn + '\n'
	cmd += 'loadHDF5chann:' + chann_fn + '\n'
	cmd += 'setChanResolution:1,4,4,40' + '\n'
	cmd += 'setChanAbsOffset:,1,0,0,0' + '\n'
	cmd += 'loadHDF5seg:' + seg_fn + '\n'
	cmd += 'setSegResolution:1,4,4,40' + '\n'
	cmd += 'setSegAbsOffset:1,0,0,0' + '\n'
	cmd += 'mesh' + '\n'
	cmd += 'quit' + '\n'

	cmd_fn = get_cmd_fn()
	with open(cmd_fn, 'w') as f:
		f.write(cmd)

def get_cmd_fn():
	return os.path.join(os.getcwd(), 'omni.cmd')

def get_tempdir():
	return os.path.join(os.path.expanduser('~'), 'Desktop')

def get_rootdir():
	return os.path.split(os.getcwd())[1]

def get_omni_fn():
	dir = get_rootdir()
	return dir + '.omni'

def get_omni_files():
	return get_omni_fn() + '.files'

def move_temp_to_cwd(fn):
	temp_path = os.path.join(get_tempdir(), fn)
	new_path = os.path.join(os.getcwd(), fn)
	if os.path.isdir(new_path):
		shutil.rmtree(new_path)
	shutil.move(temp_path, new_path)

def move_omni_project():
	move_temp_to_cwd(get_omni_fn())
	move_temp_to_cwd(get_omni_files())

def omnify():
	os.system("~/seungmount/Omni/omni/omni --headless --cmdfile='omni.cmd'")

def main(chann_fn, seg_fn):
	temp_omni_fn = os.path.join(get_tempdir(), get_omni_fn())
	write_cmd_file(temp_omni_fn, chann_fn, seg_fn)
	omnify()
	move_omni_project()

if __name__ == '__main__':
	assert len(sys.argv) > 2
	chann_fn = sys.argv[1]
	seg_fn = sys.argv[2]
	main(chann_fn, seg_fn)
