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

from send_input import LEFT_PAD, RIGHT_PAD, keypress2vector, NO_INPUT
from models.simple_lstm_nn import neural_network, one2one_model

# Constants
np.set_printoptions(threshold=np.nan)
DEBUG_DELAY = False
DEBUG_PRESSED_KEYS = False


def process_image(img):
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

def save_data(images, keyboardInputs):
	now = datetime.now().strftime("%Y%m%d%H%M%S")
	# Get current path, remove 'app' folder from it. Now we have root.
	root = '\\'.join(os.path.abspath(os.curdir).split('\\')[0:-1])
	img = f"{root}\\data\\images\\images-{now}"
	keyboard = f"{root}\\data\\keyboard\\keyboard-{now}.txt"

	np.savez(img, *images)
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


def capture_input():
	was_human = False
	left_ctrl = keypress2vector(LEFT_PAD)
	right_ctrl = keypress2vector(RIGHT_PAD)
	bomb = 0,

	combined = np.concatenate((left_ctrl, right_ctrl, bomb))

	if not np.array_equal(combined, NO_INPUT):
		print(f"Input: {combined}")
		was_human = True

	return combined, was_human


class Brain:
	def __init__(self, nn, image_buffer, controls):
		self._nn = nn
		self._image_buffer = image_buffer
		self._controls = controls

	@classmethod
	def create(cls):
		nn = neural_network(one2one_model)

		return cls(nn, None, None)

	def send_image(self, image):
		self._image_buffer = image

	def send_controls(self, controls):
		self._controls = controls

	def learn(self):
		nn_input = np.append(self._controls, self._image_buffer)
		nn_input = nn_input.reshape((1, len(nn_input)))

		controls = self._controls.reshape((1, len(self._controls)))

		# TODO: Maybe we should try to do predict here also
		# FIXME: This is probably wrong. Input should not contain same controls as output.
		#self._nn.fit(x=nn_input, y=controls, epochs=1)

	def play(self):
		return
		nn_input = np.append(self._controls, self._image_buffer)

		controls = self._nn.predict(x=nn_input)
		print("predict:", controls)


def main():
	# Debugging delayd
	last_time = time.time()
	sct = mss()
	window = {'left': 0, 'top': 0, 'width': 800, 'height': 600}
	windowHandle = win32gui.FindWindow(None, r'Geometry Wars: Retro Evolved')
	images = []
	keyboardInputs = []

	if windowHandle:
		# Make sure the window is right size and position as both can vary.
		win32gui.MoveWindow(windowHandle, 0, 0, 800, 600, True)
		win32gui.SetForegroundWindow(windowHandle)
	else:
		print('Window not found.')

	print("Getting a proper mental state...")
	brain = Brain.create()

	print('Recording!')
	while True:
		if DEBUG_DELAY:
			now = time.time()
			print("delay " + str(now-last_time))
			last_time = now

		# Captures any keyboard input
		# TODO: No bomb in inputs yet
		inputs, was_human = capture_input()

		brain.send_controls(inputs)

		sct_img = sct.grab(window)
		img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
		img = process_image(img)
		images.append(img)

		brain.send_image(img)

		if was_human:
			brain.learn()
		else:
			brain.play()

		cv2.imshow('Q to quit!', img)
		if cv2.waitKey(25) & 0xFF == ord('q'):
			cv2.destroyAllWindows()
			save_data(images, inputs)
			break

main()