import ctypes
import time
import keyboard


# Blinks the Num/Caps Lock lamps on keyboard

"""

https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes

- Virtual Keycodes, from windows.h

Load .dll once before function to avoid unnecessary calls !

"""
user32 = ctypes.WinDLL('user32')

caps_lock = 0x14
num_lock = 0x90
scroll_lock = 0x91


def blink():
    keyboard.send("caps lock")
    keyboard.send("num lock")


def lock_toggler(key):
    print('on') if user32.GetKeyState(key) else print('off')


while True:
    blink()
    # Blink interval
    time.sleep(0.5)
