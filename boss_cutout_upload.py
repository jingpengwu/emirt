# Copyright 2016 The Johns Hopkins University Applied Physics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This example shows how to work with the Boss' cutout service.  We post a tiny random matrix to the Boss and read it back
While only a 3D matrix is shown, 4D data with a time component is supported as well.
Matrices should be in ZYX or TZYX format.
"""
from intern.remote.boss import BossRemote
from intern.resource.boss.resource import *
import numpy as np
import h5py
import matplotlib.pyplot as plt
from requests import HTTPError

# valid configuration file exists at ~/.intern/intern.cfg.
rmt = BossRemote()

# To see Resources, go to https://api.theboss.io/v0.8/mgmt/resources
COLL_NAME = 'team2_waypoint'
EXP_NAME = 'pinky10'
CHAN_NAME = 'segmentation_proofread'

# Create or get a channel to write to
chan_setup = ChannelResource(CHAN_NAME, COLL_NAME, EXP_NAME, 
				type='annotation', 
				description='Manually proofread segmentation.', 
				datatype='uint64',
				sources=['segmentation'],
				creator='tmacrina')
try:
	chan_actual = rmt.get_project(chan_setup)
except HTTPError:
	chan_actual = rmt.create_project(chan_setup)

print('Data model setup.')

# Note that the numpy matrix is in Z, Y, X order.
# data = numpy.random.randint(1, 3000, (5, 4, 8))
# data = data.astype(numpy.uint16)
fn = '/usr/people/tmacrina/seungmount/Omni/TracerTasks/pinky/evaluation/' + \
		'170123_pinky10_golden/' + \
		'chunk_19585-21632_22657-24704_4003-4258_proofread_170213_smallstuff.h5'
f = h5py.File(fn, "r")
# Data size limit - breaking into 128^3 chunks below
# data = np.array(f["/main"][:254,:,:])
# # Ranges use the Python convention where the number after the : is the stop
# # value.  Thus, x_rng specifies x values where: 0 <= x < 8.
# x_rng = [20689, 20689+2048]
# y_rng = [27335, 27335+2048]
# z_rng = [2, 2+254]
# JHU-APL didn't upload all 256 z slices of segmentation properly at waypoint
# there are only 254 slices they captured

chunk = (128,128,128)
for i in range(0,2048,chunk[0]):
	for j in range(0,2048,chunk[1]):
		for k in range(0,254,chunk[2]):
			i_end = i+chunk[0] if i+chunk[0] < 2048 else 2048
			j_end = j+chunk[1] if j+chunk[1] < 2048 else 2048
			k_end = k+chunk[2] if k+chunk[2] < 254 else 254
			x_rng = [i+20689, 20689+i_end]
			y_rng = [j+27335, 27335+j_end]
			z_rng = [k+2, 2+k_end]
			print(i,j,k)
			data = np.array(f["/main"][k:k_end,j:j_end,i:i_end]).astype(np.uint64)
			# Upload the cutout to the channel.
			rmt.create_cutout(chan_actual, 0, x_rng, y_rng, z_rng, data)

# Verify that the cutout uploaded correctly.
# cutout_data = rmt.get_cutout(chan_actual, 0, x_rng, y_rng, z_rng)
# numpy.testing.assert_array_equal(data, cutout_data)

# print('Cutout uploaded and verified.')

# Double check coordinates
# COLL_NAME = 'team2_waypoint'
# EXP_NAME = 'pinky10'
# # CHAN_NAME = 'segmentation_proofread'
# CHAN_NAME = 'em'
# chan_setup = ChannelResource(CHAN_NAME, COLL_NAME, EXP_NAME, 'image', 
# 															datatype='uint8')
# chan_actual = rmt.get_project(chan_setup)

# pylab.ion()
# z_rng = [1, 2]
# cutout_data = rmt.get_cutout(chan_actual, 0, x_rng, y_rng, z_rng)
# plt.imshow(cutout_data[0,:,:], cmap='gray')
# plt.figure()
# data = np.array(f["/main"][0,:,:])
# plt.imshow(data)