from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy as np

from configuration import Config
from game.geometry_wars import geometry_wars
# TODO: Import rest later
from models.convolution_nn.convolution_nn import convolution_model
from utils.load_data import load_data
from utils.model_utility import draw_graph, load_model, minify_images

from collections import namedtuple

class Resolution(namedtuple("Resolution", "width height")):
    pass


if __name__ == "__main__":
    # Initial configs
    config = Config.default()

    resolution = Resolution(width=320, height=240)

    lb = LabelBinarizer()
    images, keyboards = load_data(config, start_index = 0, stop_index=0)
    images = minify_images(resolution, images)
    nsamples, ny, nx = images.shape

    # Even more configs
    model_name = "convolution_model_89D"
    config.add_model(f"{model_name}_{nx}_{ny}")

    keyboards = lb.fit_transform(keyboards)
    np.save('nn_classes.npy', lb.classes_)
    # for i in lb.classes_:
    #     print(i)
    num_classes = len(lb.classes_)

    # Rewrite to optimize memory
    # images = images.reshape((nsamples,nx*ny))
    images, x_test, keyboards, y_test = train_test_split(images[..., np.newaxis], keyboards, test_size=0.1)

    # m = convolution_model((nx,ny,1), num_classes)
    m = load_model(config)
    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    m.summary()

    while True:
        #TODO: append history
        history = m.fit(images, keyboards, epochs = 1, batch_size = 32,
                            validation_data = (x_test, y_test))

        # Save model
        with open(config.model_json, "w") as json_file:
            json_file.write(m.to_json())
        m.save_weights(config.model_weights)

    draw_graph(history, config.model_graph)