# https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
import ctypes
import time

import copy
import keyboard
import numpy as np

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
    #                     t tr  r br  b bl  l tl
	top         =np.array((1, 0, 0, 0, 0, 0, 0, 0)),
	bottom      =np.array((0, 0, 0, 0, 1, 0, 0, 0)),
	left        =np.array((0, 0, 0, 0, 0, 0, 1, 0)),
	right       =np.array((0, 0, 1, 0, 0, 0, 0, 0)),
	top_right   =np.array((0, 1, 0, 0, 0, 0, 0, 0)),
	top_left    =np.array((0, 0, 0, 0, 0, 0, 0, 1)),
	bottom_right=np.array((0, 0, 0, 1, 0, 0, 0, 0)),
	bottom_left =np.array((0, 0, 0, 0, 0, 1, 0, 0)),
	)

NO_INPUT = np.array((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

def keypress2vector(mapping):
    pressed = ""

    # Loop only first 4 keys. Expects keys to be in certain order
    # so that 'pressed' is built properly.
    for key in tuple(mapping.keys())[:4]:
        if keyboard.is_pressed(key):
            pressed += key

    try:
        return VECTORS[mapping[pressed]]
    except KeyError:
        return NO_INPUT[:8]

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))