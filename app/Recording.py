import sys, os
import numpy as np
import cv2 # pip install opencv-python
from mss.windows import MSS as mss # pip install mss
from PIL import Image
from PIL import ImageGrab
import win32gui
import time
from datetime import datetime

sys.path.insert(0, os.path.abspath(''))
from utils.recording_utility import pressed_keys, process_image

# Constants
np.set_printoptions(threshold=np.nan)
DEBUG_DELAY = True
DEBUG_PRESSED_KEYS = False

def save_data(images, keyboardInputs):
	now = datetime.now().strftime("%Y%m%d%H%M%S")
	# Get current path, remove 'app' folder from it. Now we have root.
	root = '\\'.join(os.path.abspath(os.curdir).split('\\')[0:-1])
	img = f"{root}\\data\\images\\images-{now}"
	keyboard = f"{root}\\data\\keyboard\\keyboard-{now}.txt"
	
	np.savez_compressed(img, *images)
	f = open(keyboard,"w")
	for k in keyboardInputs:
		if k:
			try:
				f.write(" ".join(sorted(k)))
			except:
				print(k)
				f.write("blank")
		else:
			f.write("blank")
		f.write("\n")

	f.close()


def main():
	# Debugging delay
	last_time = time.time()
	sct = mss()
	window = {'left': 0, 'top': 0, 'width': 800, 'height': 600}
	windowHandle = win32gui.FindWindow(None, 'Geometry Wars: Retro Evolved')
	images = []
	keyboardInputs = []

	if windowHandle:
		# Make sure the window is right size and position as both can vary.
		win32gui.MoveWindow(windowHandle, *window.values(), True)
		win32gui.SetForegroundWindow(windowHandle)
	else:
		print('Window not found.')

	print('Recording!')
	while 1:
		if DEBUG_DELAY:
			now = time.time()
			print("delay " + str(now-last_time))
			last_time = now

		pressed = pressed_keys()
		if DEBUG_PRESSED_KEYS:
			print(pressed)
		
		sct_img = sct.grab(window)
		img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
		img = process_image(img)
		images.append(img)
		keyboardInputs.append(pressed)

		cv2.imshow('Q to quit!', img)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			save_data(images, keyboardInputs)
			break

if __name__ == "__main__":
   main()
