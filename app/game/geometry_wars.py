"""
This module encapsulates locating the game, getting proper handlers and managing
window position and size.
"""

import time
import win32gui, win32com.client

class GameError(Exception): pass

class GameWindow:
    def __init__(self, handle, window):
        assert handle is not None
        self._handle = None
        self._window = None  # FIXME: should probably get values from the window

    @property
    def window(self):
        return self._window


def geometry_wars(width=800, height=600, left=0, top=0):
    window_handle = win32gui.FindWindow(None, 'Geometry Wars: Retro Evolved')

    window = {'left': left, 'top': top, 'width': width, 'height': height}

    if window_handle:
        # Make sure the window is right size and position as both can vary.
        win32gui.MoveWindow(window_handle, *window.values(), True)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(window_handle)
        time.sleep(.1)
    else:
        raise GameError('Geometry wars could not be found!')

    return GameWindow(window_handle, window)


if __name__ == "__main__":
    gw = geometry_wars()
    print(gw.window)