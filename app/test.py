from configuration import Config
from utils.load_data import load_data

import cv2
import time

config = Config.default()
images, keyboards = load_data(config, start_index = 2, stop_index=3)

for img in images:
	print(img.__class__)
	print(img.shape)
	cv2.imshow('Q to quit!', img)
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break
	# time.sleep(.1)


# images = process_images(images, resolution)