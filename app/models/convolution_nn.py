from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Dense, Flatten

def convolution_model(input_shape, output_shape):
    m = Sequential()

    m.add(Conv2D(filters = 32,
                 kernel_size = (5, 5),
                 activation = 'relu',
                 padding = 'same',
                 input_shape=input_shape) )
    m.add(MaxPooling2D(4,4))
    m.add(Conv2D(filters = 16,
                 kernel_size = (5, 5),
                 padding = 'same',
                 activation = 'relu') )
    m.add(MaxPooling2D(4,4))
    m.add(Conv2D(filters = 8,
                 kernel_size = (5, 5),
                 padding = 'same',
                 activation = 'relu') )
    m.add(Flatten())
    m.add(Dense(128, activation = 'relu'))
    m.add(Dense(output_shape, activation='sigmoid'))

    return m