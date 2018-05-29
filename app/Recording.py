import numpy as np
import cv2 # pip install opencv-python
from mss.windows import MSS as mss # pip install mss
from PIL import Image
from PIL import ImageGrab
import win32gui
import time
from datetime import datetime
import keyboard
import os

from sendInput import LEFT_PAD, RIGHT_PAD, keypress2vector, NO_INPUT

# Constants
np.set_printoptions(threshold=np.nan)
DEBUG_DELAY = False
DEBUG_PRESSED_KEYS = False


def processImage(img):
	# To grayscale
	img = cv2.cvtColor(np.array(img, dtype = np.uint8), cv2.COLOR_BGR2GRAY)
	# To binary
	thresh, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	# Filter particles
	closing = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
	opening = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
	img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, closing)
	img = cv2.morphologyEx(img, cv2.MORPH_OPEN, opening)

	return img

def main():
	# Debugging delay
	last_time = time.time()
	index = 0
	data = ""
	f = ""
	sct = mss()
	window = {'left': 0, 'top': 0, 'width': 800, 'height': 600}
	windowHandle = win32gui.FindWindow(None, r'Geometry Wars: Retro Evolved')
	now = datetime.now().strftime("%Y%m%d%H%M%S")
	# Get current path, remove 'app' folder from it. Now we have root.
	root = '\\'.join(os.path.abspath(os.curdir).split('\\')[0:-1])
	filepath = f"{root}\\data\\gameData-{now}.txt"
	# Create file to data folder
	# f = open(filepath,"w+")

	if windowHandle:
		# Make sure the window is right size and position as both can vary.
		win32gui.MoveWindow(windowHandle, 0, 0, 800, 600, True)
	else:
		print('Window not found.')

	print('Recording!')
	while 1:
		index += 1
		if DEBUG_DELAY:
			now = time.time()
			print("delay " + str(now-last_time))
			last_time = now

		left_ctrl = keypress2vector(LEFT_PAD)
		right_ctrl = keypress2vector(RIGHT_PAD)
		if left_ctrl != NO_INPUT or right_ctrl != NO_INPUT:
			print(f'left: {left_ctrl}, right: {right_ctrl}')

		sct_img = sct.grab(window)
		img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
		img = processImage(img)
		# img.tofile(filepath, format='%4d', sep=",")

		cv2.imshow('Q to quit!', img)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			# f.close()
			break

main()