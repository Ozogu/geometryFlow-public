import pprint
import os
from pathlib import Path


class Config:
    def __init__(self, root):
        assert os.path.isabs(root)
        self._root = Path(root)

    @classmethod
    def default(cls):
        config = cls(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
        config.data = config.root / 'data'
        config.images = config.data / 'images'
        config.keyboard = config.data / 'keyboard'

        assert str(config.root).endswith('geometryFlow')

        return config

    def add_model(self, model_name):
        self.model_data = config.data / model_name
        self.model_json = config.model_data / f"{model_name}.json"
        self.model_weights = config.model_data / f"{model_name}.h5"
        self.model_graph = config.model_data / f"{model_name}.pdf"

    def __repr__(self):
        simple = {'Config().%s' % k:str(v) for k,v in self.__dict__.items() if not k.startswith('_')}
        as_string = pprint.pformat(simple, indent=4).replace('{', ' ').replace('}', ' ')
        return 'Config(%r)\n%s' % (self._root, as_string)

    @property
    def root(self):
        return self._root


if __name__ == "__main__":
    config = Config.default()
    config.add_model("test_model")

    print(config)