import keras

"""
    @param x: a numpy array of controls and images for 1 second time window.
    @param y: a numpy array of controls. Vector (length 17) should look like:
        [left controls (t tr r br b bl l tl), right controls (t tr r br b bl l tl), bomb]
"""

CONTROLS_SIZE = 17
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def model(t_x, t_y, n_a, input_size):
    """
    @param t_x: input size for controls and images
    @param t_x: output size for controls
    @param n_a: hidden state size of the LSTM
    @param input_size: size of input vector, which contains controls and images
    """
    x = keras.layers.Input(shape=(t_x, CONTROLS_SIZE + WINDOW_WIDTH * WINDOW_HEIGHT))

    outputs = []
    a0 = a = keras.layers.LSTM(n_a)(x)


    return keras.models.Model(inputs=[x, a0], outputs=outputs)

if __name__ == "__main__":
    model(5, 1, 32, CONTROLS_SIZE)