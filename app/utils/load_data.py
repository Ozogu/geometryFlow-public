import numpy as np
import os
import re

def exctract_date(file_name):
	return file_name.split('-')[1].split('.')[0]

def load_data():
	# Get current path, remove 'app' and 'utils' folder from it. Now we have root.
	root_folder = os.path.abspath(os.curdir).split('\\')[:-2]

	images_folder = "\\".join(root_folder + ['data'] + ['images'])
	keyboard_folder = "\\".join(root_folder + ['data'] + ['keyboard'])

	image_files = os.listdir(images_folder)
	keyboard_files = os.listdir(keyboard_folder)

	images = []
	keyboards = []

	# Loop through image files
	for i in range(0,len(image_files)):
		image_file = image_files[i]
		# The date matches perfectly with corresponding keyboard file
		date = exctract_date(image_file)
		# Write regex rule to find the keyboard file
		r = re.compile(f".*{date}.*")
		keyboard_candidates = filter(r.match, keyboard_files)
		if len(keyboard_candidates) != 1:
			raise ValueError(f'There are not exactly 1 keyboard files with date: {date}!')
		keyboard_file = list(keyboard_candidates)[0]

		images.append(np.load(images_folder + '\\' + image_file))
		with open(keyboard_folder + '\\' + keyboard_file) as kf:
			keyboards.append(kf.readlines())

	return images, keyboards