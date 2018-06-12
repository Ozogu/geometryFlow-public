from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy as np
import cv2
import time

from configuration import Config
from game.geometry_wars import geometry_wars
from game.controllers import Keyboard, Classifier17D

# TODO: Import rest later
from models.convolution_nn.convolution_nn import convolution_model
from utils.load_data import load_data
from utils.model_utility import draw_graph, load_model, minify_images

from collections import namedtuple

DEBUG_IMAGES = False

class Resolution(namedtuple("Resolution", "width height")):
    @classmethod
    def from_shape(cls, shape):
        return cls(height=shape[0], width=shape[-1])

    @property
    def shape(self):
        return (self.height, self.width)


def process_images(images, resolution):
    def process(image):
        image = cv2.cvtColor(np.array(image, dtype = np.uint8), cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, dsize=resolution, interpolation=cv2.INTER_CUBIC)

        return image

    images = [process(i) for i in images]
    return np.array(images)


if __name__ == "__main__":
    # Initial configs
    config = Config.default()

    resolution = Resolution(width=320, height=240)

    images, keyboards = load_data(config, start_index = 0, stop_index=1)
    images = process_images(images, resolution)

    if DEBUG_IMAGES:
        for img in images:
            cv2.imshow('Q to quit!', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    nsamples, nx, ny = images.shape  # FIXME: Why this keeps switching dimensions??
    assert (nx, ny) == resolution.shape

    # Even more configs
    model_name = "convolution_model_17D"
    config.add_model(f"{model_name}_{ny}_{nx}")

    controller = Keyboard(keyboards)
    output_vector_classes = controller.classify(Classifier17D())

    # Rewrite to optimize memory
    # images = images.reshape((nsamples,nx*ny))
    images, x_test, output_vector_classes, y_test = train_test_split(images[..., np.newaxis], output_vector_classes, test_size=0.1)

    try:
        m = load_model(config)
    except:
        m = convolution_model((nx,ny,1), output_vector_classes.shape[-1])
        with open(config.model_json, "w") as json_file:
            json_file.write(m.to_json())

    m.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    try:
        m.load_weights(config.model_weights)
    except OSError:
        pass

    m.summary()

    while True:
        #TODO: append history
        history = m.fit(images, output_vector_classes, epochs = 100, batch_size = 32,
                            validation_data = (x_test, y_test))

        m.save_weights(config.model_weights)

    draw_graph(history, config.model_graph)