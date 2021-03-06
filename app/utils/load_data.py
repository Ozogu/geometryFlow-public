##
## Designed to load data outputted from commit 580c7e12 recordings!
##

import numpy as np
import os
import re

def exctract_date(file_name):
	return file_name.split('-')[1].split('.')[0]

def load_data(datapaths, start_index = 0, stop_index = 0):
	print(f'Reading data paths:\n - {datapaths.images}\n - {datapaths.keyboard}')

	# Weird monstrosity
	image_files = os.listdir(datapaths.images)
	keyboard_files = os.listdir(datapaths.keyboard)

	images = np.array([])
	keyboards = []

	# Make sure loop stays inbounds.
	if len(image_files) < stop_index:
		stop_index = len(image_files)

	# Loop through image files
	for i in range(start_index, (stop_index or len(image_files))):
		image_file = image_files[i]
		# The date matches perfectly with corresponding keyboard file
		date = exctract_date(image_file)
		# Write regex rule to find the keyboard file
		r = re.compile(f".*{date}.*")
		keyboard_candidates = list(filter(r.match, keyboard_files))
		if len(keyboard_candidates) != 1:
			raise ValueError(f'There are not exactly 1 keyboard files with date: {date}!')
		keyboard_file = keyboard_candidates[0]

		print(f'loading {image_file}')
		loaded_files = np.load(datapaths.images / image_file)
		temp = []
		for f in loaded_files:
			temp.append(loaded_files[f])

		print(f'loading {keyboard_file}')
		stack = np.stack(temp)
		if images.size != 0:
			images = np.concatenate((images,stack), axis=0)
		else:
			images = stack

		with open(datapaths.keyboard / keyboard_file) as kf:
			# Strip newlines
			keyboards += map(str.strip, kf.readlines())

	return images, keyboards
