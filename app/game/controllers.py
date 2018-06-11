import abc
import keyboard
import numpy as np


class Joystick(metaclass=abc.ABCMeta):
    def __init__(self, **directions):
        self._direction = directions

    @abc.abstractmethod
    def to_vector(self, directions):
        ''' '''

class Joystick8D(Joystick):
    # Direction for left pad. Dictionary keys are order sensitive!
    LEFT_PAD = dict(
        w='top',
        s='bottom',
        a='left',
        d='right',
        wd='top_right',
        sd='bottom_right',
        sa='bottom_left',
        wa='top_left',
    )

    # Direction for right pad. Dictionary keys are order sensitive!
    RIGHT_PAD = dict(
        up='top',
        down='bottom',
        left='left',
        right='right',
        upright='top_right',
        downright='bottom_right',
        downleft='bottom_left',
        upleft='top_left',
        )

    # Input vectors for NN
    VECTORS = dict(
        #                      t  tr r  br b  bl l tl
        top         =np.array((1, 0, 0, 0, 0, 0, 0, 0)),
        bottom      =np.array((0, 0, 0, 0, 1, 0, 0, 0)),
        left        =np.array((0, 0, 0, 0, 0, 0, 1, 0)),
        right       =np.array((0, 0, 1, 0, 0, 0, 0, 0)),
        top_right   =np.array((0, 1, 0, 0, 0, 0, 0, 0)),
        top_left    =np.array((0, 0, 0, 0, 0, 0, 0, 1)),
        bottom_right=np.array((0, 0, 0, 1, 0, 0, 0, 0)),
        bottom_left =np.array((0, 0, 0, 0, 0, 1, 0, 0)),
        )

    # Default for no input.
    NO_INPUT = np.array((0, 0, 0, 0, 0, 0, 0, 0))

    def __init__(self, mapping):
        self._mapping = mapping

    @classmethod
    def from_left(cls):
        return cls(cls.LEFT_PAD)

    @classmethod
    def from_right(cls):
        return cls(cls.RIGHT_PAD)

    def to_vector(self, directions):
        pressed = "".join(b for b in self._mapping if b in directions.split())

        try:
            return self.VECTORS[self._mapping[pressed]]
        except KeyError:
            return self.NO_INPUT


class Classifier17D:
    def __init__(self):
        self._left_pad = Joystick8D.from_left()
        self._right_pad = Joystick8D.from_right()

    def __call__(self, keypresses):
        left_ctrl = self._left_pad.to_vector(keypresses)
        right_ctrl = self._right_pad.to_vector(keypresses)
        bomb = (1, ) if "space" in keypresses else (0, )

        combined = np.concatenate((left_ctrl, right_ctrl, bomb))

        return combined


class Controller:
    # http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
    KEY_MAP = {
        'esc': 0x01,
        'enter': 0x1C,
        'w': 0x11,
        's': 0x1F,
        'a': 0x1E,
        'd': 0x20,
        'up': 0xC8,
        'down': 0xD0,
        'left': 0xCB,
        'right': 0xCD,
        'space': 0x39
    }

    KEYS = list(KEY_MAP.keys())
    KEYS.remove('esc')
    KEYS.remove('enter')

    def __init__(self, snapshots=None):
        assert isinstance(snapshots, (type(None), list))
        self._input_snapshots = snapshots or []

    def position(self):
        pressed = []
        for k in self.KEYS:
            if keyboard.is_pressed(k):
                pressed.append(k)

        return pressed

    def output_vector(self):
        pass

    def snapshot(self):
        self._input_snapshots.append(self.position())

    def classify(self, classifier_func):
        return np.array([classifier_func(m) for m in self._input_snapshots])

        # FIXME: Why this doesn't work??
        #return np.array(map(classifier_func, self._input_snapshots))

    @property
    def inputs(self):
        return self._input_snapshots