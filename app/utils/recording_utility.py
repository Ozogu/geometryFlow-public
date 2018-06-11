import sys, os
import cv2
import numpy as np
import keyboard

sys.path.insert(0, os.path.abspath('..'))
from utils.send_input import KEY_MAP

keys = list(KEY_MAP.keys())
keys.remove('esc')
keys.remove('enter')

def pressed_keys():
	pressed = []
	for k in keys:
		if keyboard.is_pressed(k):
			pressed.append(k)

	return pressed

def process_image(img, new_size=(800,600)):
	# To grayscale
	img = cv2.cvtColor(np.array(img, dtype = np.uint8), cv2.COLOR_BGR2GRAY)
	img = cv2.resize(img, dsize=(320,240), interpolation=cv2.INTER_CUBIC)

	return img