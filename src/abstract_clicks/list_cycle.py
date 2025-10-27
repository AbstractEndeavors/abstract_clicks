from pynput import keyboard
from .imports import *
from .utils import *
import cv2
import os
import time
import platform
import threading
import subprocess
import pyperclip
import pyautogui
import mss
from PIL import Image
import pytesseract

import subprocess
from pynput import keyboard

# Example creds



# Global state
clip_mgr = ClipboardManager()
clip_mgr.start_monitoring()
index = 0
ctrl_held = False

def on_press(key):
    global index, ctrl_held
    try:
        if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
            ctrl_held = True
        elif key.char == 'v' and ctrl_held:
            # Prepare next cred BEFORE system paste consumes it
            cred = login_creds[index % len(login_creds)]
            clip_mgr.custom_copy(cred)
            print(f"Ctrl+V detected → preloaded: {cred}")
            index += 1
            # Now let OS paste it naturally
    except AttributeError:
        pass

def on_release(key):
    global ctrl_held
    if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
        ctrl_held = False

with keyboard.Listener() as listener:
    listener.join()
