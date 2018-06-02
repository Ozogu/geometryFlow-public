# Path hack.
import sys, os
sys.path.insert(0, os.path.abspath(''))

from utils.send_input import press_key, release_key, KEY_MAP
import win32gui
import time

# Have geometry wars open and in game

# Focus window
windowHandle = win32gui.FindWindow(None, r'Geometry WArs: Retro Evolved')
win32gui.SetForegroundWindow(windowHandle)
time.sleep(.1)

# Close menu screen
press_key(KEY_MAP['esc'])
time.sleep(.1)
release_key(KEY_MAP['esc'])

# Play the game..
press_key(KEY_MAP['w'])
press_key(KEY_MAP['d'])
press_key(KEY_MAP['upArrow'])
press_key(KEY_MAP['leftArrow'])
time.sleep(5)
release_key(KEY_MAP['w'])
release_key(KEY_MAP['d'])
release_key(KEY_MAP['upArrow'])
release_key(KEY_MAP['leftArrow'])
