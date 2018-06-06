
import os
from pathlib import Path


class Config:
    def __init__(self, root):
        assert os.path.isabs(root)
        assert os.path.split(root)[-1] == 'geometryFlow'  # FIXME: Should not hardcode
        self._root = Path(root)

    @classmethod
    def default(cls):
        return cls(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

    def __repr__(self):
        return 'Config(%r)' % self._root

    @property
    def root(self):
        return self._root


if __name__ == "__main__":
    config = Config.default()
    print(config.root)

    config.data = config.root / 'data'

    print(config.data)