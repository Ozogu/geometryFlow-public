import numpy as np
import cv2 # pip install opencv-python
from mss.windows import MSS as mss # pip install mss
from PIL import Image
from PIL import ImageGrab
import win32gui
import time
import keyboard

from sendInput import KEY_MAP

# Constants
DEBUG_DELAY = False
KEYS = list(KEY_MAP.keys())

def pressedKeys():
	pressed = []
	for k in KEYS:
		if keyboard.is_pressed(k): pressed.append(k)

	return pressed

def main():
	windowHandle = win32gui.FindWindow(None, r'Geometry WArs: Retro Evolved')
	if not windowHandle:
		print('Window not found, returning.')
		return

	sct = mss()
	window = {'left': 0, 'top': 0, 'width': 800, 'height': 600}
	# Make sure the window is right size and position as both can vary.
	win32gui.MoveWindow(windowHandle, 0, 0, 800, 600, True)

	print('Recording!')
	# Debugging delay 
	last_time = time.time()
	while 1:
		if DEBUG_DELAY:
			now = time.time()
			print("delay " + str(now-last_time))
			last_time = now

		print(pressedKeys())
		sct_img = sct.grab(window)
		img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
		cv2.imshow('Q to quit!', np.array(img))
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			break
			
main()