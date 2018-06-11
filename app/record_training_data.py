import sys, os
import numpy as np
import cv2
from mss.windows import MSS as mss # pip install mss
from PIL import Image
from PIL import ImageGrab
import win32gui
import time
from datetime import datetime
from inputs import devices 

from configuration import Config
from game.geometry_wars import geometry_wars
from game.controllers import Keyboard
from game.controllers import Controller
from game.controllers import InputDevice


# Constants
np.set_printoptions(threshold=np.nan)
DEBUG_DELAY = False
DEBUG_PRESSED_KEYS = False

def save_data(config, images, device_inputs):
    np.savez_compressed(config.train_images, *images)
    f = open(config.train_ctrl,"w")
    for inputs in device_inputs:
        f.write(inputs)
        f.write("\n")

    f.close()


def main():
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    config = Config.default()
    config.add_model("convolution_model_17d_320_240")
    config.train_images = config.images / f'images-{now}'
    config.train_ctrl = config.keyboard / f'keyboard-{now}.txt'

    game = geometry_wars()

    input_device = InputDevice
    if (devices.gamepads):
        input_device = Controller()
    else:
        input_device = Keyboard()

    # Debugging delay
    last_time = time.time()
    sct = mss()
    images = []

    print('Recording!')
    while True:
        if DEBUG_DELAY:
            now = time.time()
            print("delay " + str(now-last_time))
            last_time = now

        input_device.snapshot()

        sct_img = sct.grab(game.window)
        img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        img = np.array(img)
        images.append(img)

        cv2.imshow('Q to quit!', np.array(img, dtype=np.uint8))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            save_data(config, images, input_device.inputs)
            break

if __name__ == "__main__":
   main()
