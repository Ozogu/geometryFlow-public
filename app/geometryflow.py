import sys, os
from mss.windows import MSS as mss
from PIL import Image
import win32gui, win32com.client
import time
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import joblib
import cv2
import keyboard

# Path hack.
sys.path.insert(0, os.path.abspath(''))

from utils.send_input import press_key, release_key, KEY_MAP
from utils.recording_utility import process_image
from utils.model_utility import load_model

DEBUG_KEYBOARD = False
DEBUG_TIMES = False

def press_and_release(current_keys, last_keys):
	if DEBUG_KEYBOARD: print(current_keys)
	if last_keys and last_keys != 'blank':
		for k in last_keys.split(' '):
			release_key(KEY_MAP[k])

	if current_keys and current_keys != 'blank':
		for k in current_keys.split(' '):
			press_key(KEY_MAP[k])

def main():
	windowHandle = win32gui.FindWindow(None, 'Geometry Wars: Retro Evolved')
	sct = mss()
	window = {'left': 0, 'top': 0, 'width': 800, 'height': 600}
	lb = LabelEncoder()
	last_keys = ''
            
	if windowHandle:
		# Make sure the window is right size and position as both can vary.
		win32gui.MoveWindow(windowHandle, *window.values(), True)
		shell = win32com.client.Dispatch("WScript.Shell")
		shell.SendKeys('%')
		win32gui.SetForegroundWindow(windowHandle)
		time.sleep(.1)
	else:
		raise ValueError('Geometry wars could not be found!')

	lb.classes_ = np.load('models/convolution_nn/nn_classes.npy')
	m = load_model('models/convolution_nn/convolution_model',240,320)

	# Close menu screen
	press_key(KEY_MAP['esc'])
	time.sleep(.1)
	release_key(KEY_MAP['esc'])
	time.sleep(.1)

	last_time = time.time()
	while True:
		# Get image
		sct_img = sct.grab(window)
		img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
		img = process_image(img).reshape((1,240,320,1))

		# Reshape for the model
		processed = time.time()-last_time
		if DEBUG_TIMES: print("Processing took " + str(processed))
		# Predict
		prediction = m.predict_classes(img)
		if DEBUG_TIMES: print("Predicting took " + str(time.time()-processed-last_time))
		# Converts the integer to array with keys the classifier wants to be pressed.
		current_keys = lb.inverse_transform(prediction)[0]
		press_and_release(current_keys, last_keys)
		last_keys = current_keys

		if DEBUG_TIMES: print("Total " + str(time.time()-last_time))
		last_time = time.time()

		if keyboard.is_pressed('q'):
			print("Q detected! Quitting!")
			break


if __name__ == "__main__":
   main()