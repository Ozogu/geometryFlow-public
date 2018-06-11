import sys, os
import numpy as np
import cv2 # pip install opencv-python
from mss.windows import MSS as mss # pip install mss
from PIL import Image
from PIL import ImageGrab
import win32gui
import time
from datetime import datetime

from configuration import Config
from game.geometry_wars import geometry_wars
from game.controllers import Controller


# Constants
np.set_printoptions(threshold=np.nan)
DEBUG_DELAY = False
DEBUG_PRESSED_KEYS = False

def save_data(config, images, keyboard_inputs):
    np.savez_compressed(config.train_images, *images)
    f = open(config.train_ctrl,"w")
    for k in keyboard_inputs:
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
    now = datetime.now().strftime("%Y%m%d%H%M%S")

    config = Config.default()
    config.add_model("convolution_model_17d_320_240")
    config.train_images = config.images / f'images-{now}'
    config.train_ctrl = config.keyboard / f'keyboard-{now}.txt'

    game = geometry_wars()
    controller = Controller()

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

        controller.snapshot()

        sct_img = sct.grab(game.window)
        img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        images.append(img)

        cv2.imshow('Q to quit!', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            save_data(config, images, controller.inputs)
            break

if __name__ == "__main__":
   main()
