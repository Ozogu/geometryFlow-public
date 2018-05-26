from sendInput import PressKey, ReleaseKey, KEY_MAP
import win32gui
import time

# Have geometry wars open and in game

# Focus window
windowHandle = win32gui.FindWindow(None, r'Geometry WArs: Retro Evolved')
win32gui.SetForegroundWindow(windowHandle)
time.sleep(.1)

# Close menu screen
PressKey(KEY_MAP['esc'])
time.sleep(.1)
ReleaseKey(KEY_MAP['esc'])

# Play the game..
PressKey(KEY_MAP['w'])
PressKey(KEY_MAP['d'])
PressKey(KEY_MAP['upArrow'])
PressKey(KEY_MAP['leftArrow'])
time.sleep(5)
ReleaseKey(KEY_MAP['w'])
ReleaseKey(KEY_MAP['d'])
ReleaseKey(KEY_MAP['upArrow'])
ReleaseKey(KEY_MAP['leftArrow'])
