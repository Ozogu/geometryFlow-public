import cv2
import numpy as np

def minify_images(y,x,images):
    tmp = []
    for img in images:
        tmp.append(cv2.resize(img, dsize=(y, x), interpolation=cv2.INTER_CUBIC))

    return np.array(tmp)