import sys, os
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Dense, Flatten

# Path hack.
sys.path.insert(0, os.path.abspath('../..'))
from utils.load_data import load_data
from utils.model_utility import draw_graph, load_model

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

if __name__ == "__main__":
    lb = LabelBinarizer()
    images, keyboards = load_data(start_index = 2)
    # images = minify_images(240,320,images)
    nsamples, nx, ny = images.shape

    keyboards = lb.fit_transform(keyboards)
    np.save('nn_classes.npy', lb.classes_)
    num_classes = len(lb.classes_)
    
    # Rewrite to optimize memory
    # images = images.reshape((nsamples,nx*ny))
    images, x_test, keyboards, y_test = train_test_split(images[..., np.newaxis], keyboards, test_size=0.1)

    model_name = "convolution_model"
    # m = convolution_model((nx,ny,1), num_classes)
    m = load_model(model_name, nx, ny)
    m.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    m.summary()

    history = m.fit(images, keyboards, epochs = 1, batch_size = 1,
                        validation_data = (x_test, y_test))

    # Save model
    with open(f"{model_name}_{nx}_{ny}.json", "w") as json_file:
        json_file.write(m.to_json())
    m.save_weights(f"{model_name}_{nx}_{ny}.h5")

    draw_graph(history, f"{model_name}_{nx}_{ny}")