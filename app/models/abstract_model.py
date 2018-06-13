import abc

class AbstractModel(metaclass=abc.ABCMeta):
    # TODO: commented to be made optional and/or with default value

    # Model
    model_name = abc.abstractproperty
    input_device = abc.abstractproperty

    # Data
    use_preprosessed_data = abc.abstractproperty
    # load_start_index = abc.abstractproperty
    # load_stop_index = abc.abstractproperty
    input_device_shape = abc.abstractproperty
    image_shape = abc.abstractproperty # (x,y,z)

    # Paths
    model_data = self.model_name
    model_json = abc.abstractproperty
    model_weights = abc.abstractproperty
    model_graph = abc.abstractproperty
    model_classes = abc.abstractproperty

    # training
    epochs = abc.abstractproperty
    loss_function = abc.abstractproperty
    optimizer = abc.abstractproperty
    # test_size = abc.abstractproperty
    # metrics = abc.abstractproperty

    def __init__(self, config):
        self.config(config)

    @abc.abstractmethod
    def model_structure(self):
        ''' '''

    @abc.abstractmethod
    def process_input_data(self, data):
        ''' '''

    def config(self, config):
        config.model_data = config.model_data / self.model_data
        config.model_json = config.model_data / self.model_json
        config.model_weights = config.model_data / self.model_weights

