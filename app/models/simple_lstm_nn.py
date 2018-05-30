import keras

"""
    @param x: a numpy array of controls and images for 1 second time window.
    @param y: a numpy array of controls. Vector (length 17) should look like:
        [left controls (t tr r br b bl l tl), right controls (t tr r br b bl l tl), bomb]
"""

CONTROLS_SIZE = 17
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def one2one_model(x_n, y_n):
    """
    Creates a traditional 1-to-1 model, where input is controls + image and output is controls.

    @param x_n: input size for controls and images
    @param y_n: output size for controls
    """
    # Input layer, where input size is 17 + 800 * 600
    x = keras.layers.Input(shape=(x_n, 1))

    # 1st hidden layer, with less units and ReLU activation (to keep values between 0..1)
    y = keras.layers.Dense(int(x_n / 160))(x)
    y = keras.layers.Activation(activation='relu')(y)

    # 2nd hidden layer, with less units and ReLU activation (to keep values between 0..1)
    y = keras.layers.Dense(int(x_n / 640))(y)
    y = keras.layers.Activation(activation='relu')(y)

    # Last layer with softmax activation
    y = keras.layers.Dense(17)(y)
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

if __name__ == "__main__":
    input_vector_size = CONTROLS_SIZE + WINDOW_WIDTH * WINDOW_HEIGHT

    m = one2one_model(x_n=input_vector_size, y_n=CONTROLS_SIZE)
    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])