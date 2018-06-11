from configuration import Config
from utils.load_data import load_data

import cv2
import time

config = Config.default()
images, keyboards = load_data(config, start_index = 0, stop_index=0)

for img in images:
    cv2.imshow('Q to quit!', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break