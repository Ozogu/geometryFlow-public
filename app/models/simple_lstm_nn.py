import keras
import sys, os
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy as np

# Path hack.
sys.path.insert(0, os.path.abspath('..'))
from utils.load_data import load_data
from utils.draw_graph import draw_graph
from utils.minify_images import minify_images

"""
    @param x: a numpy array of controls and images for 1 second time window.
    @param y: a numpy array of controls. Vector (length 17) should look like:
        [left controls (t tr r br b bl l tl), right controls (t tr r br b bl l tl), bomb]
"""

CONTROLS_SIZE = 17
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
MODEL_NAME = "one2one_model"


def one2one_model(x_n, y_n):
    """
    Creates a traditional 1-to-1 model, where input is controls + image and output is controls.

    @param x_n: input size for controls and images
    @param y_n: output size for controls
    """
    # Input layer, where input size is x_n
    x = keras.layers.Input(shape=(x_n, ))

    # 1st hidden layer, with less units and ReLU activation (to keep values between 0..1)
    y = keras.layers.Dense(int(x_n / 160))(x)
    y = keras.layers.Activation(activation='relu')(y)

    # 2nd hidden layer, with less units and ReLU activation (to keep values between 0..1)
    y = keras.layers.Dense(int(x_n / 640))(y)
    y = keras.layers.Activation(activation='relu')(y)

    # Last layer with softmax activation
    y = keras.layers.Dense(y_n)(y)
    y = keras.layers.Softmax()(y)

    return keras.Model(inputs=x, outputs=y)


def many2one_lstm_model(t_x, t_y, n_a, input_size):
    """
    @param t_x: input size for controls and images
    @param t_x: output size for controls
    @param n_a: hidden state size of the LSTM
    @param input_size: size of input vector, which contains controls and images
    """
    x = keras.layers.Input(shape=(t_x, CONTROLS_SIZE + WINDOW_WIDTH * WINDOW_HEIGHT, 1))

    a0 = a = keras.layers.LSTM(n_a)(x)

    x = keras.layers.TimeDistributed(keras.layers.Dense(1, activation="sigmoid"))(a)

    return keras.models.Model(inputs=[x, a0], outputs=x)

def neural_network(model_func):
    lb = LabelBinarizer()
    images, keyboards = load_data()
    images = minify_images(240,320,images)
    nsamples, nx, ny = images.shape

    keyboards = lb.fit_transform(keyboards)
    np.save('nn_classes.npy', lb.classes_)

    # TODO: Develop method to convert the keyboard data to designed multi input format.
    m = one2one_model(x_n=nx*ny, y_n=len(lb.classes_))
    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    m.summary()
    
    # Rewrite to optimize memory
    images = images.reshape((nsamples,nx*ny))
    images, x_test, keyboards, y_test = train_test_split(images, keyboards, test_size=0.1)

    history = m.fit(images, keyboards, epochs = 2, batch_size = 1,
                        validation_data = (x_test, y_test))

    draw_graph(history)

    # Save model
    with open(f"{MODEL_NAME}_{nx}_{ny}.json", "w") as json_file:
        json_file.write(m.to_json())
    m.save_weights(f"{MODEL_NAME}_{nx}_{ny}")

    return m

if __name__ == "__main__":
    nn = neural_network(one2one_model)