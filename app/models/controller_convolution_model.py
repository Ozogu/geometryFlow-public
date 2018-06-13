from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Dense, Flatten

from abstract_model import AbstractModel

class ControllerConvolutionModel(AbstractModel):
    # Model
    model_name = "controller_convolution_model"
    input_device = "controller"

    # Data
    use_preprosessed_data = False
    # load_start_index = abc.abstractproperty
    # load_stop_index = abc.abstractproperty
    input_device_shape = (5)
    image_shape = (320,240,1) # (x,y,z)

    # Paths
    model_data = self.model_name
    model_json = f"{self.model_name}.json"
    model_weights = f"{self.model_name}.h5"
    model_graph = f"{self.model_name}.pdf"
    model_classes = f"{self.model_name}.npy"

    # training
    epochs = 20
    loss_function = "categorical_crossentropy"
    optimizer = "sgd"
    test_size = .1
    metrics = "accuracy"

    def __init__(self):
        super().__init__()


    def model_structure(self):
        m = Sequential()

        m.add(Conv2D(filters = 32,
                     kernel_size = (5, 5),
                     activation = 'relu',
                     padding = 'same',
                     input_shape=self.input_device_shape) )
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
        m.add(Dense(self.image_shape, activation='sigmoid'))

        return m